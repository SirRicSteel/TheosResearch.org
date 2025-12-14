"""
THEOS Memory Engine

Implements wisdom accumulation through:
- DecisionRecord schema with full audit trail
- SQLite durable storage (WAL mode)
- Vector-like retrieval using cosine similarity (no external dependencies)
- Promotion gates, decay, and supersession
- Two-pass I→A→D cycle that consults accumulated wisdom

Python 3.10+
No external dependencies
"""

from __future__ import annotations

import json
import math
import os
import sqlite3
import time
import uuid
import hashlib
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional, Tuple


# ---------------------------
# Utilities
# ---------------------------

def now_iso_local() -> str:
    # Store ISO with local offset if desired; for simplicity use UTC
    return datetime.now(timezone.utc).isoformat()

def sha256_text(s: str) -> str:
    norm = " ".join(s.strip().lower().split())
    return hashlib.sha256(norm.encode("utf-8")).hexdigest()

def safe_float(x: Any, default: float = 0.0) -> float:
    try:
        return float(x)
    except Exception:
        return default

def cosine_similarity(a: List[float], b: List[float]) -> float:
    # Robust cosine for small vectors
    if not a or not b or len(a) != len(b):
        return 0.0
    dot = 0.0
    na = 0.0
    nb = 0.0
    for i in range(len(a)):
        dot += a[i] * b[i]
        na += a[i] * a[i]
        nb += b[i] * b[i]
    if na <= 0.0 or nb <= 0.0:
        return 0.0
    return dot / (math.sqrt(na) * math.sqrt(nb))


# ---------------------------
# DecisionRecord
# ---------------------------

@dataclass
class DecisionRecord:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now_iso_local)
    engine_version: str = "theos-0.1"
    model_version: str = "unknown"

    query: Dict[str, Any] = field(default_factory=dict)
    context: Dict[str, Any] = field(default_factory=dict)

    cycle: Dict[str, Any] = field(default_factory=dict)
    decision: Dict[str, Any] = field(default_factory=dict)
    governance: Dict[str, Any] = field(default_factory=dict)
    evaluation: Dict[str, Any] = field(default_factory=dict)
    lifecycle: Dict[str, Any] = field(default_factory=dict)

    # Store embedding inline for MVP; production would store in a vector index
    embedding: List[float] = field(default_factory=list)

    def to_json(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False)

    @staticmethod
    def from_json(s: str) -> "DecisionRecord":
        obj = json.loads(s)
        # Backwards tolerant
        return DecisionRecord(
            id=obj.get("id", str(uuid.uuid4())),
            created_at=obj.get("created_at", now_iso_local()),
            engine_version=obj.get("engine_version", "theos-0.1"),
            model_version=obj.get("model_version", "unknown"),
            query=obj.get("query", {}) or {},
            context=obj.get("context", {}) or {},
            cycle=obj.get("cycle", {}) or {},
            decision=obj.get("decision", {}) or {},
            governance=obj.get("governance", {}) or {},
            evaluation=obj.get("evaluation", {}) or {},
            lifecycle=obj.get("lifecycle", {}) or {},
            embedding=obj.get("embedding", []) or [],
        )


# ---------------------------
# SQLite store (Tier B/C)
# ---------------------------

class TheosStore:
    def __init__(self, db_path: str = "theos_memory.sqlite"):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.conn.execute("PRAGMA journal_mode=WAL;")
        self.conn.execute("PRAGMA synchronous=NORMAL;")
        self._init_schema()

    def close(self) -> None:
        try:
            self.conn.close()
        except Exception:
            pass

    def _init_schema(self) -> None:
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS decision_records (
                id TEXT PRIMARY KEY,
                created_at TEXT NOT NULL,
                engine_version TEXT,
                model_version TEXT,
                query_hash TEXT,
                domain TEXT,
                intent TEXT,
                risk_level TEXT,
                tier TEXT,
                promotion_state TEXT,
                decay_weight REAL,
                validated INTEGER,
                outcome_score REAL,
                superseded_by TEXT,
                embedding_json TEXT,
                record_json TEXT NOT NULL
            );
            """
        )
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_query_hash ON decision_records(query_hash);")
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_promotion_state ON decision_records(promotion_state);")
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_tier ON decision_records(tier);")
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_created_at ON decision_records(created_at);")
        self.conn.commit()

    @staticmethod
    def _get_flat_fields(rec: DecisionRecord) -> Dict[str, Any]:
        q = rec.query or {}
        c = rec.context or {}
        cf = (c.get("fingerprint") or {})
        lc = rec.lifecycle or {}
        ev = rec.evaluation or {}

        domain = q.get("domain", [])
        intent = q.get("intent", [])
        if isinstance(domain, list):
            domain_s = ",".join(map(str, domain))
        else:
            domain_s = str(domain) if domain else ""
        if isinstance(intent, list):
            intent_s = ",".join(map(str, intent))
        else:
            intent_s = str(intent) if intent else ""

        return {
            "query_hash": q.get("hash") or "",
            "domain": domain_s,
            "intent": intent_s,
            "risk_level": str(cf.get("risk_level") or ""),
            "tier": str(lc.get("tier") or "B"),
            "promotion_state": str(lc.get("promotion_state") or "draft"),
            "decay_weight": safe_float(lc.get("decay_weight", 1.0), 1.0),
            "validated": 1 if bool((ev.get("validated") is True) or (ev.get("validated") == 1)) else 0,
            "outcome_score": safe_float((ev.get("outcome_score") if ev else None), None) if ev else None,
            "superseded_by": lc.get("superseded_by"),
        }

    def upsert(self, rec: DecisionRecord) -> None:
        flat = self._get_flat_fields(rec)
        emb_json = json.dumps(rec.embedding)
        self.conn.execute(
            """
            INSERT INTO decision_records (
                id, created_at, engine_version, model_version,
                query_hash, domain, intent, risk_level,
                tier, promotion_state, decay_weight, validated,
                outcome_score, superseded_by, embedding_json, record_json
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                created_at=excluded.created_at,
                engine_version=excluded.engine_version,
                model_version=excluded.model_version,
                query_hash=excluded.query_hash,
                domain=excluded.domain,
                intent=excluded.intent,
                risk_level=excluded.risk_level,
                tier=excluded.tier,
                promotion_state=excluded.promotion_state,
                decay_weight=excluded.decay_weight,
                validated=excluded.validated,
                outcome_score=excluded.outcome_score,
                superseded_by=excluded.superseded_by,
                embedding_json=excluded.embedding_json,
                record_json=excluded.record_json
            ;
            """,
            (
                rec.id, rec.created_at, rec.engine_version, rec.model_version,
                flat["query_hash"], flat["domain"], flat["intent"], flat["risk_level"],
                flat["tier"], flat["promotion_state"], flat["decay_weight"], flat["validated"],
                flat["outcome_score"], flat["superseded_by"], emb_json, rec.to_json()
            )
        )
        self.conn.commit()

    def get(self, record_id: str) -> Optional[DecisionRecord]:
        cur = self.conn.execute(
            "SELECT record_json FROM decision_records WHERE id = ?;",
            (record_id,)
        )
        row = cur.fetchone()
        if not row:
            return None
        return DecisionRecord.from_json(row[0])

    def list_recent(self, limit: int = 20, promotion_state: Optional[str] = None) -> List[DecisionRecord]:
        if promotion_state:
            cur = self.conn.execute(
                "SELECT record_json FROM decision_records WHERE promotion_state=? ORDER BY created_at DESC LIMIT ?;",
                (promotion_state, limit)
            )
        else:
            cur = self.conn.execute(
                "SELECT record_json FROM decision_records ORDER BY created_at DESC LIMIT ?;",
                (limit,)
            )
        return [DecisionRecord.from_json(r[0]) for r in cur.fetchall()]

    def search_similar(
        self,
        query_embedding: List[float],
        top_k: int = 10,
        min_decay_weight: float = 0.05,
        allowed_tiers: Tuple[str, ...] = ("C", "B"),
        allowed_promotion_states: Tuple[str, ...] = ("promoted", "candidate"),
        domain_filter: Optional[str] = None,
        max_scan: int = 2000,
    ) -> List[Tuple[DecisionRecord, float]]:
        """
        MVP approach: scan up to max_scan records, compute cosine similarity.
        Production: use a real vector index (FAISS, etc.)
        """
        placeholders_tiers = ",".join("?" for _ in allowed_tiers)
        placeholders_states = ",".join("?" for _ in allowed_promotion_states)

        params: List[Any] = list(allowed_tiers) + list(allowed_promotion_states) + [min_decay_weight, max_scan]

        sql = f"""
            SELECT embedding_json, record_json, decay_weight
            FROM decision_records
            WHERE tier IN ({placeholders_tiers})
              AND promotion_state IN ({placeholders_states})
              AND decay_weight >= ?
            ORDER BY created_at DESC
            LIMIT ?;
        """

        cur = self.conn.execute(sql, params)
        scored: List[Tuple[DecisionRecord, float]] = []
        for emb_json, rec_json, decay_w in cur.fetchall():
            try:
                emb = json.loads(emb_json) if emb_json else []
            except Exception:
                emb = []
            rec = DecisionRecord.from_json(rec_json)

            # Optional domain filter (simple string contains in stored domain CSV)
            if domain_filter:
                dom = (rec.query or {}).get("domain", [])
                dom_s = ",".join(dom) if isinstance(dom, list) else str(dom)
                if domain_filter not in dom_s:
                    continue

            sim = cosine_similarity(query_embedding, emb)
            sim *= safe_float(decay_w, 1.0)
            scored.append((rec, sim))

        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:top_k]

    def apply_decay(
        self,
        half_life_days: float = 30.0,
        floor: float = 0.02,
        promotion_state: Optional[str] = "promoted",
    ) -> None:
        """
        Simple exponential decay of decay_weight based on age.
        """
        now_ts = time.time()
        cur = self.conn.execute(
            "SELECT id, created_at, decay_weight FROM decision_records WHERE promotion_state=?;",
            (promotion_state,)
        )
        rows = cur.fetchall()
        for rid, created_at, decay_w in rows:
            try:
                created_dt = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
                age_days = (datetime.now(timezone.utc) - created_dt.astimezone(timezone.utc)).total_seconds() / 86400.0
            except Exception:
                age_days = 0.0

            # decay factor for half-life
            # weight_new = weight_old * 0.5^(age/half_life)
            decay_factor = math.pow(0.5, age_days / max(half_life_days, 1e-6))
            new_w = max(floor, safe_float(decay_w, 1.0) * decay_factor)

            self.conn.execute(
                "UPDATE decision_records SET decay_weight=? WHERE id=?;",
                (new_w, rid)
            )
        self.conn.commit()


# ---------------------------
# Embedding (pluggable)
# ---------------------------

def simple_hash_embedding(text: str, dim: int = 128) -> List[float]:
    """
    Deterministic, dependency-free embedding. Not semantic, but works as a scaffold.
    Replace with a real embedder later (OpenAI embeddings, sentence-transformers, etc.)
    """
    h = hashlib.sha256(text.encode("utf-8")).digest()
    # Expand to dim via repeated hashing
    out = [0.0] * dim
    seed = h
    i = 0
    while i < dim:
        seed = hashlib.sha256(seed).digest()
        for b in seed:
            if i >= dim:
                break
            out[i] = (b - 128) / 128.0
            i += 1
    # normalize
    norm = math.sqrt(sum(x * x for x in out)) or 1.0
    return [x / norm for x in out]


# ---------------------------
# Governor: validation + promotion
# ---------------------------

@dataclass
class GateThresholds:
    min_coherence: float = 0.75
    max_risk: float = 0.30
    min_constraint_adherence: float = 0.90
    require_counterexample_test: bool = True
    stability_required: bool = True


def compute_self_scores_stub(answer_text: str) -> Dict[str, float]:
    """
    Replace this with real scoring: rubric model, unit tests, eval harness, etc.
    """
    # Very naive heuristics; do NOT treat as real evaluation.
    length = len(answer_text.strip())
    coherence = 0.70 + min(0.25, length / 2000.0 * 0.25)
    risk = 0.10  # default low
    constraint_adherence = 0.95
    helpfulness = 0.75
    return {
        "coherence": float(min(1.0, coherence)),
        "risk": float(max(0.0, min(1.0, risk))),
        "constraint_adherence": float(min(1.0, constraint_adherence)),
        "helpfulness": float(min(1.0, helpfulness)),
    }


def validate_record(rec: DecisionRecord, thresholds: GateThresholds) -> Tuple[bool, List[str]]:
    reasons: List[str] = []
    ev = rec.evaluation or {}
    ss = (ev.get("self_score") or {})
    coherence = safe_float(ss.get("coherence"), 0.0)
    risk = safe_float(ss.get("risk"), 1.0)
    ca = safe_float(ss.get("constraint_adherence"), 0.0)

    if coherence < thresholds.min_coherence:
        reasons.append(f"coherence {coherence:.2f} < {thresholds.min_coherence:.2f}")
    if risk > thresholds.max_risk:
        reasons.append(f"risk {risk:.2f} > {thresholds.max_risk:.2f}")
    if ca < thresholds.min_constraint_adherence:
        reasons.append(f"constraint_adherence {ca:.2f} < {thresholds.min_constraint_adherence:.2f}")

    # Counterexample gate: look for deduction.tests with "counterexample"
    if thresholds.require_counterexample_test:
        ded = (rec.cycle or {}).get("deduction") or {}
        tests = ded.get("tests") or []
        found = any(("counterexample" in (t.get("test","").lower())) for t in tests if isinstance(t, dict))
        if not found:
            reasons.append("missing counterexample test")

    # Stability gate: if pass #2 contradicts pass #1 without explanation
    if thresholds.stability_required:
        cyc = rec.cycle or {}
        # optional: store pass1_answer, pass2_answer
        pass1 = cyc.get("pass1_answer")
        pass2 = cyc.get("pass2_answer")
        if pass1 and pass2 and (pass1.strip() != pass2.strip()):
            # look for explanation token
            rationale = (rec.decision or {}).get("rationale_summary") or []
            rationale_text = " ".join(rationale) if isinstance(rationale, list) else str(rationale)
            if "changed" not in rationale_text.lower() and "revised" not in rationale_text.lower():
                reasons.append("answer changed between passes without explanation")

    ok = len(reasons) == 0
    return ok, reasons


def promote_or_demote(rec: DecisionRecord, ok: bool, reasons: List[str]) -> DecisionRecord:
    lc = rec.lifecycle or {}
    ev = rec.evaluation or {}
    if ok:
        lc["tier"] = "C"
        lc["promotion_state"] = "promoted"
        ev["validated"] = True
    else:
        # keep as candidate in B unless severe
        lc["tier"] = lc.get("tier") or "B"
        lc["promotion_state"] = "candidate"
        ev["validated"] = False
        # attach reasons for audit
        ev["validation_notes"] = reasons
    rec.lifecycle = lc
    rec.evaluation = ev
    return rec


# ---------------------------
# THEOS Engine skeleton (I → A → D, two-pass)
# ---------------------------

class TheosEngine:
    def __init__(
        self,
        store: TheosStore,
        embed_fn: Callable[[str], List[float]] = simple_hash_embedding,
        thresholds: GateThresholds = GateThresholds(),
    ):
        self.store = store
        self.embed_fn = embed_fn
        self.thresholds = thresholds

    def retrieve_priors(
        self,
        query_text: str,
        domain_filter: Optional[str] = None,
        top_k: int = 8
    ) -> List[DecisionRecord]:
        emb = self.embed_fn(query_text)
        results = self.store.search_similar(
            query_embedding=emb,
            top_k=top_k,
            domain_filter=domain_filter,
            allowed_tiers=("C", "B"),
            allowed_promotion_states=("promoted", "candidate"),
        )
        return [r for (r, score) in results if score > 0.0]

    # --- The three phases (stubs) ---
    def induction(self, query_text: str, priors: List[DecisionRecord]) -> Dict[str, Any]:
        observations = []
        patterns = []
        # Minimal: extract recurring constraints/principles from priors
        for p in priors[:5]:
            gov = p.governance or {}
            principles = gov.get("principles_applied") or []
            if principles:
                observations.append(f"prior principles: {principles}")
        patterns.append("use structured multi-pass reasoning")
        return {"observations": observations, "pattern_hypotheses": patterns}

    def abduction(self, query_text: str, induction_out: Dict[str, Any]) -> Dict[str, Any]:
        # Hypothesis generation stub
        candidates = [
            {"h": "Answer directly with structured reasoning + constraints", "prior": 0.6},
            {"h": "Ask clarifying question", "prior": 0.2},
            {"h": "Refuse if unsafe", "prior": 0.2},
        ]
        selected = max(candidates, key=lambda x: x["prior"])["h"]
        return {"candidate_hypotheses": candidates, "selected": selected}

    def deduction(self, query_text: str, abduct_out: Dict[str, Any]) -> Dict[str, Any]:
        # Test stub: always include counterexample test
        tests = [
            {"test": "counterexample check", "result": "pass"},
            {"test": "constraint compliance", "result": "pass"},
        ]
        failure_modes = ["overclaiming", "missing constraints", "hallucinating specifics"]
        return {"tests": tests, "failure_modes_considered": failure_modes}

    def synthesize_answer_stub(self, query_text: str, priors: List[DecisionRecord]) -> str:
        """
        Replace this with your actual model call.
        This stub just demonstrates wiring.
        """
        # Minimal “answer” showing priors influence:
        bullets = []
        for p in priors[:3]:
            rs = (p.decision or {}).get("rationale_summary") or []
            if isinstance(rs, list) and rs:
                bullets.append(f"- prior rationale: {rs[0]}")
        prior_block = "\n".join(bullets)
        return (
            f"THEOS-structured response to: {query_text}\n"
            f"{prior_block}\n"
            f"(Replace synthesize_answer_stub with your model call.)"
        )

    def run_two_pass(
        self,
        query_text: str,
        domain: Optional[List[str]] = None,
        intent: Optional[List[str]] = None,
        risk_level: str = "low",
    ) -> DecisionRecord:
        qhash = sha256_text(query_text)
        domain = domain or []
        intent = intent or []

        # Retrieve priors BEFORE pass 1
        priors = self.retrieve_priors(query_text, domain_filter=(domain[0] if domain else None), top_k=8)

        # Pass #1
        ind1 = self.induction(query_text, priors)
        abd1 = self.abduction(query_text, ind1)
        ded1 = self.deduction(query_text, abd1)
        pass1_answer = self.synthesize_answer_stub(query_text, priors)

        # Feed back into pass #2 input (your "momentary past")
        pass2_input = f"{query_text}\n\n[PASS1_OUTPUT]\n{pass1_answer}"

        # Retrieve priors again using pass2_input (optional but useful)
        priors2 = self.retrieve_priors(pass2_input, domain_filter=(domain[0] if domain else None), top_k=8)

        ind2 = self.induction(pass2_input, priors2)
        abd2 = self.abduction(pass2_input, ind2)
        ded2 = self.deduction(pass2_input, abd2)
        pass2_answer = self.synthesize_answer_stub(pass2_input, priors2)

        # Build DecisionRecord
        emb = self.embed_fn(query_text)

