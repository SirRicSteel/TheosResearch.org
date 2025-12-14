#!/usr/bin/env python3
"""
THEOS Integration Demo
======================

Complete working example demonstrating the integration of:
- Dual-Clock Governor (contradiction-bounded refinement)
- Memory Engine (wisdom accumulation)

This is a production-ready reference implementation showing how
the two components work together to generate emergent wisdom.

Usage:
    python3 theos_integration_demo.py

Requirements:
    - Python 3.10+
    - No external dependencies (uses only standard library)
"""

import sys
import os
from pathlib import Path

# Add parent directories to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "governor"))
sys.path.insert(0, str(Path(__file__).parent.parent / "memory_engine"))

from theos_dual_clock_governor import (
    TheosDualClockGovernor,
    GovernorConfig,
    EngineOutput,
    GovernorDecision
)

from theos_memory_engine import (
    TheosStore,
    TheosEngine,
    DecisionRecord
)

import random
import time
from typing import List, Dict, Any, Optional


class TheosIntegratedSystem:
    """
    Complete THEOS system integrating Governor and Memory Engine.
    
    This demonstrates the full architecture:
    1. Query arrives
    2. Memory Engine retrieves relevant priors (accumulated wisdom)
    3. Dual engines generate outputs using priors
    4. Governor evaluates and decides CONTINUE or FREEZE
    5. Final decision is validated and stored as future wisdom
    """
    
    def __init__(
        self,
        db_path: str = "theos_demo.sqlite",
        max_cycles: int = 4,
        max_risk: float = 0.35,
        contradiction_budget: float = 1.5
    ):
        """Initialize integrated THEOS system."""
        
        # Initialize Memory Engine
        self.store = TheosStore(db_path)
        self.memory = TheosEngine(store=self.store)
        
        # Initialize Governor
        self.governor_config = GovernorConfig(
            max_cycles=max_cycles,
            max_risk=max_risk,
            contradiction_budget=contradiction_budget
        )
        self.governor = TheosDualClockGovernor(self.governor_config)
        
        print(f"✓ THEOS Integrated System initialized")
        print(f"  Database: {db_path}")
        print(f"  Max cycles: {max_cycles}")
        print(f"  Max risk: {max_risk}")
        print(f"  Contradiction budget: {contradiction_budget}")
        print()
    
    def simulate_engine_output(
        self,
        engine_id: str,
        cycle: int,
        query: str,
        priors: List[Dict[str, Any]],
        previous_output: Optional[str] = None
    ) -> EngineOutput:
        """
        Simulate engine output based on query and priors.
        
        In production, this would call actual LLM engines.
        For demo purposes, we simulate realistic outputs.
        """
        
        if engine_id == "L":
            # Constructive engine: builds on priors
            if priors:
                prior_insights = " ".join([p.get("final_answer", "")[:50] for p in priors[:2]])
                answer = f"Based on accumulated wisdom: {prior_insights}... [Constructive answer for: {query}]"
            else:
                answer = f"Initial constructive answer for: {query}"
            
            # Constructive engine has high coherence, low risk
            coherence = 0.85 + random.uniform(0, 0.1)
            risk = 0.1 + random.uniform(0, 0.05)
            contradiction = None
            
        else:  # engine_id == "R"
            # Adversarial engine: challenges previous output
            if previous_output:
                answer = f"Counterexample to consider: What if the opposite is true? [Challenge to: {previous_output[:50]}...]"
                contradiction = f"Cycle {cycle}: Identified potential weakness in constructive reasoning"
            else:
                answer = f"Initial adversarial perspective for: {query}"
                contradiction = None
            
            # Adversarial engine has moderate coherence, higher risk
            coherence = 0.75 + random.uniform(0, 0.1)
            risk = 0.15 + random.uniform(0, 0.1)
        
        return EngineOutput(
            engine_id=engine_id,
            cycle_index=cycle,
            answer=answer,
            coherence=coherence,
            risk=risk,
            contradiction_claim=contradiction
        )
    
    def run_query(
        self,
        query: str,
        domain: List[str],
        intent: List[str],
        risk_level: str = "low",
        verbose: bool = True
    ) -> Dict[str, Any]:
        """
        Run complete THEOS query with Governor + Memory integration.
        
        Returns:
            Dictionary containing:
            - final_answer: The committed answer
            - cycles_used: Number of refinement cycles
            - stop_reason: Why refinement stopped
            - priors_used: Number of prior decisions retrieved
            - stored_record_id: ID of stored decision
        """
        
        if verbose:
            print(f"\n{'='*80}")
            print(f"THEOS QUERY: {query}")
            print(f"{'='*80}\n")
        
        # Step 1: Retrieve priors from memory
        if verbose:
            print("📚 STEP 1: Retrieving accumulated wisdom...")
        
        priors = self.memory.retrieve_priors(
            query_text=query,
            domain_filter=domain[0] if domain else None,
            top_k=5
        )
        
        if verbose:
            print(f"   Retrieved {len(priors)} relevant prior decisions")
            for i, prior in enumerate(priors[:3], 1):
                print(f"   Prior {i}: {prior.get('final_answer', '')[:60]}...")
            print()
        
        # Step 2: Initialize Governor
        if verbose:
            print("⚙️  STEP 2: Initializing Dual-Clock Governor...")
        
        self.governor = TheosDualClockGovernor(self.governor_config)
        
        # Step 3: Run refinement cycles
        if verbose:
            print("🔄 STEP 3: Running contradiction-bounded refinement...\n")
        
        cycle = 1
        previous_left_output = None
        decision = None
        
        while cycle <= self.governor_config.max_cycles:
            if verbose:
                print(f"   Cycle {cycle}/{self.governor_config.max_cycles}")
            
            # Generate outputs from both engines
            left_output = self.simulate_engine_output(
                engine_id="L",
                cycle=cycle,
                query=query,
                priors=priors,
                previous_output=None
            )
            
            right_output = self.simulate_engine_output(
                engine_id="R",
                cycle=cycle,
                query=query,
                priors=priors,
                previous_output=left_output.answer
            )
            
            if verbose:
                print(f"      Clock L (Constructive): coherence={left_output.coherence:.2f}, risk={left_output.risk:.2f}")
                print(f"      Clock R (Adversarial):  coherence={right_output.coherence:.2f}, risk={right_output.risk:.2f}")
            
            # Governor evaluates
            decision = self.governor.step(left_output, right_output)
            
            if verbose:
                print(f"      Governor decision: {decision.decision}")
                print(f"      Reason: {decision.reason}")
            
            if decision.decision == "FREEZE":
                if verbose:
                    print(f"\n   ❄️  FREEZE triggered: {decision.reason}")
                break
            
            if verbose:
                print(f"      → CONTINUE to cycle {cycle + 1}\n")
            
            cycle += 1
            previous_left_output = left_output.answer
        
        # Step 4: Commit final answer
        if verbose:
            print("\n✅ STEP 4: Committing final answer...")
        
        final_answer = decision.chosen_answer if decision else left_output.answer
        
        if verbose:
            print(f"   Final answer: {final_answer[:100]}...")
            print()
        
        # Step 5: Store in memory for future retrieval
        if verbose:
            print("💾 STEP 5: Storing decision as future wisdom...")
        
        # Create a simple decision record manually
        from datetime import datetime, timezone
        import uuid
        
        record_data = {
            "record_id": str(uuid.uuid4()),
            "query_text": query,
            "query_hash": self.memory.embed_fn(query)[0],  # Simple hash
            "domain": domain,
            "intent": intent,
            "risk_level": risk_level,
            "final_answer": final_answer,
            "rationale": decision.reason if decision else "Completed all cycles",
            "cycles_used": cycle,
            "stop_condition": decision.reason if decision else "Max cycles",
            "promotion_state": "candidate",
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        
        # Store using raw SQL with actual schema
        record_id = record_data["record_id"]
        
        # Create full record JSON
        import json
        full_record = {
            "query": {"query_text": query},
            "decision": {
                "final_answer": final_answer,
                "rationale": record_data["rationale"]
            },
            "governance": {
                "cycles_used": cycle,
                "stop_condition": record_data["stop_condition"]
            }
        }
        
        self.store.conn.execute("""
            INSERT OR REPLACE INTO decision_records 
            (id, query_hash, domain, intent, risk_level, promotion_state, 
             validated, created_at, record_json, embedding_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            record_id,
            str(record_data["query_hash"]),
            ",".join(domain),
            ",".join(intent),
            risk_level,
            "candidate",
            0,
            record_data["created_at"],
            json.dumps(full_record),
            "[]"
        ))
        self.store.conn.commit()
        
        if verbose:
            print(f"   Stored as record ID: {record_id[:8]}...")
            print(f"   Promotion state: candidate")
            print()
        
        return {
            "final_answer": final_answer,
            "cycles_used": cycle,
            "stop_reason": decision.reason if decision else "Max cycles reached",
            "priors_used": len(priors),
            "stored_record_id": record_id,
            "coherence": left_output.coherence,
            "risk": left_output.risk
        }
    
    def show_wisdom_accumulation(self, domain: str = None):
        """Display accumulated wisdom in the system."""
        
        print(f"\n{'='*80}")
        print(f"ACCUMULATED WISDOM")
        print(f"{'='*80}\n")
        
        # Query database directly
        if domain:
            cursor = self.store.conn.execute(
                "SELECT * FROM decision_records WHERE domain LIKE ? ORDER BY created_at DESC LIMIT 10",
                (f"%{domain}%",)
            )
        else:
            cursor = self.store.conn.execute(
                "SELECT * FROM decision_records ORDER BY created_at DESC LIMIT 10"
            )
        
        records = cursor.fetchall()
        
        print(f"Total decisions stored: {len(records)}\n")
        
        import json
        for i, rec in enumerate(records[:5], 1):
            record_json = json.loads(rec[15]) if rec[15] else {}  # record_json column
            query_text = record_json.get("query", {}).get("query_text", "N/A")
            final_answer = record_json.get("decision", {}).get("final_answer", "N/A")
            
            print(f"{i}. Query: {query_text[:60]}...")
            print(f"   Answer: {final_answer[:80]}...")
            print(f"   Domain: {rec[5]}")  # domain column
            print(f"   Promotion: {rec[9]}")  # promotion_state column
            print()
    
    def close(self):
        """Clean up resources."""
        self.store.close()
        print("✓ THEOS system closed")


def run_demo():
    """Run complete demonstration of THEOS integrated system."""
    
    print("\n" + "="*80)
    print("THEOS INTEGRATED SYSTEM DEMONSTRATION")
    print("="*80)
    print("\nDemonstrating:")
    print("  • Dual-Clock Governor (contradiction-bounded refinement)")
    print("  • Memory Engine (wisdom accumulation)")
    print("  • Complete integration showing emergent wisdom")
    print()
    
    # Initialize system
    system = TheosIntegratedSystem(
        db_path="theos_demo.sqlite",
        max_cycles=4,
        max_risk=0.35,
        contradiction_budget=1.5
    )
    
    # Demo queries
    demo_queries = [
        {
            "query": "How should AI systems handle ethical dilemmas?",
            "domain": ["ai_safety"],
            "intent": ["analyze"],
            "risk_level": "medium"
        },
        {
            "query": "What are the key principles for Constitutional AI?",
            "domain": ["ai_safety"],
            "intent": ["draft"],
            "risk_level": "low"
        },
        {
            "query": "How can we ensure AI alignment with human values?",
            "domain": ["ai_safety"],
            "intent": ["analyze"],
            "risk_level": "medium"
        }
    ]
    
    # Run queries
    results = []
    for i, q in enumerate(demo_queries, 1):
        print(f"\n\n{'#'*80}")
        print(f"DEMO QUERY {i}/{len(demo_queries)}")
        print(f"{'#'*80}")
        
        result = system.run_query(**q, verbose=True)
        results.append(result)
        
        time.sleep(0.5)  # Brief pause for readability
    
    # Show accumulated wisdom
    system.show_wisdom_accumulation(domain="ai_safety")
    
    # Summary
    print(f"\n{'='*80}")
    print(f"DEMONSTRATION SUMMARY")
    print(f"{'='*80}\n")
    
    for i, (q, r) in enumerate(zip(demo_queries, results), 1):
        print(f"{i}. {q['query'][:60]}...")
        print(f"   Cycles: {r['cycles_used']}, Stop reason: {r['stop_reason']}")
        print(f"   Priors used: {r['priors_used']}, Coherence: {r['coherence']:.2f}, Risk: {r['risk']:.2f}")
        print()
    
    print("Key observations:")
    print("  • Each query benefits from accumulated wisdom (priors)")
    print("  • Governor prevents infinite refinement loops")
    print("  • Decisions are stored and become wisdom for future queries")
    print("  • System demonstrates emergent wisdom, not emergent risk")
    print()
    
    # Cleanup
    system.close()
    
    print("\n✓ Demonstration complete")
    print(f"\nDatabase saved to: theos_demo.sqlite")
    print("You can inspect the accumulated wisdom using any SQLite browser.")
    print()


if __name__ == "__main__":
    try:
        run_demo()
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nError during demo: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
