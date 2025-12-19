# THEOS Integration Sketch: Medical Diagnosis Support

**Document Type:** Concrete Deployment Example  
**Date:** December 19, 2025  
**Use Case:** Claude + THEOS + Medical Knowledge Tools  

---

## Overview

This document provides a concrete example of how THEOS overlay integrates with Claude in a production environment. The use case—medical diagnosis support—is chosen because it is:

- **High-stakes** (patient safety critical)
- **Complex** (requires multi-step reasoning)
- **Tool-dependent** (needs access to medical databases, drug interaction checkers)
- **Safety-critical** (errors have serious consequences)

This integration pattern generalizes to other high-stakes domains (legal, financial, autonomous agents).

---

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    USER INTERFACE                        │
│  (Physician enters patient symptoms, history, labs)     │
└────────────────────┬────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────┐
│                  THEOS GOVERNOR                          │
│  - Monitors reasoning process                            │
│  - Controls tool access                                  │
│  - Enforces safety invariants                            │
│  - Manages contradiction budget                          │
└────────┬───────────────────────────────────┬────────────┘
         │                                   │
         ↓                                   ↓
┌──────────────────────┐          ┌──────────────────────┐
│   ENGINE L           │          │   ENGINE R           │
│   (Constructive)     │ ←──────→ │   (Adversarial)      │
│                      │          │                      │
│   Claude Sonnet 4.5  │          │   Claude Sonnet 4.5  │
│   + Medical Context  │          │   + Medical Context  │
└────────┬─────────────┘          └──────────┬───────────┘
         │                                   │
         │         ┌─────────────────┐       │
         └────────→│  TOOL GATEWAY   │←──────┘
                   │  (Governed)     │
                   └────────┬────────┘
                            │
         ┌──────────────────┼──────────────────┐
         ↓                  ↓                  ↓
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│  Medical DB     │ │  Drug Interaction│ │  Clinical       │
│  (UpToDate)     │ │  Checker         │ │  Guidelines     │
└─────────────────┘ └─────────────────┘ └─────────────────┘
```

---

## Workflow Example: Differential Diagnosis

### Input

**Physician query:**
> "Patient: 45-year-old male, presents with chest pain (8/10), radiating to left arm, shortness of breath, diaphoresis. History: hypertension, type 2 diabetes, smoker (20 pack-years). Vitals: BP 160/95, HR 110, RR 22, O2 sat 94% on room air. ECG shows ST elevation in leads II, III, aVF. Troponin pending. Generate differential diagnosis and recommend immediate management."

### Cycle 1: Initial Assessment

**Engine L (Constructive) - Induction:**
- Gathers evidence from query
- Identifies key symptoms: chest pain, ST elevation, risk factors
- **Tool request:** Access medical database for "ST elevation MI"

**Governor decision:**
- Query is in-scope (medical diagnosis)
- Tool request approved (medical database is safe for this context)
- Contradiction budget: 100 units allocated

**Tool Gateway:**
- Executes medical database query
- Returns: ST elevation myocardial infarction (STEMI) diagnostic criteria

**Engine L (Constructive) - Abduction:**
- Generates hypothesis: "Likely STEMI (inferior wall)"
- Proposes immediate management: aspirin, clopidogrel, heparin, cath lab activation

**Engine L (Constructive) - Deduction:**
- Tests hypothesis against evidence
- Checks: ST elevation pattern consistent with inferior STEMI
- Confidence: High (95%)

---

**Engine R (Adversarial) - Induction:**
- Reviews same evidence
- Identifies alternative possibilities
- **Tool request:** Access medical database for "chest pain differential"

**Governor decision:**
- Tool request approved
- Contradiction budget: 90 units remaining (10 consumed by Engine L tool use)

**Tool Gateway:**
- Executes query
- Returns: Differential includes STEMI, aortic dissection, pulmonary embolism, pericarditis

**Engine R (Adversarial) - Deduction:**
- Tests alternative hypotheses
- Aortic dissection: Possible (chest pain radiating, hypertension), but ST elevation atypical
- Pulmonary embolism: Less likely (ST elevation not typical pattern)
- Pericarditis: Unlikely (ST elevation pattern wrong, no PR depression)

**Engine R (Adversarial) - Abduction:**
- Challenges Engine L: "Have you ruled out aortic dissection? This is life-threatening and requires different management."
- Proposes additional assessment: Check blood pressure in both arms, consider CT angiography

---

**Governor measures contradiction:**
- Engine L: STEMI (95% confidence)
- Engine R: STEMI likely, but aortic dissection not ruled out (80% confidence in STEMI, 15% in dissection)
- **Contradiction score: 15 units** (moderate disagreement)

**Governor decision:**
- Contradiction above threshold (>10 units)
- Continue reasoning (budget allows)
- Cycle 1 complete

---

### Cycle 2: Refinement

**Engine L (Constructive) - Induction:**
- Acknowledges Engine R's challenge
- Reviews evidence for aortic dissection
- **Tool request:** Access clinical guidelines for "aortic dissection vs STEMI"

**Governor decision:**
- Tool request approved
- Contradiction budget: 75 units remaining

**Tool Gateway:**
- Returns: "Check blood pressure in both arms; >20 mmHg difference suggests dissection. Widened mediastinum on CXR suggests dissection."

**Engine L (Constructive) - Abduction:**
- Refines hypothesis: "STEMI is most likely, but must rule out aortic dissection before thrombolytics or anticoagulation (could be catastrophic if dissection)"
- Proposes: Check BP both arms, portable CXR, hold anticoagulation until dissection ruled out

**Engine L (Constructive) - Deduction:**
- Tests refined approach
- Safer: Avoids catastrophic error (anticoagulating a dissection)
- Slightly delays definitive STEMI treatment, but risk-benefit favors caution

---

**Engine R (Adversarial) - Induction:**
- Reviews refined approach
- Satisfied that aortic dissection is being addressed

**Engine R (Adversarial) - Deduction:**
- Tests: Is delay in STEMI treatment acceptable?
- Calculates: 5-10 minute delay for BP check and CXR vs. risk of catastrophic dissection mismanagement
- Conclusion: Acceptable risk-benefit

**Engine R (Adversarial) - Abduction:**
- Agrees with refined approach
- Adds: "If BP equal both arms and CXR normal, proceed with STEMI protocol immediately"

---

**Governor measures contradiction:**
- Engine L: STEMI with dissection ruled out (revised approach)
- Engine R: Agrees with revised approach
- **Contradiction score: 3 units** (low disagreement, convergence achieved)

**Governor decision:**
- Contradiction below threshold (<10 units)
- **STOP: Convergence achieved**
- Cycle 2 complete
- Total cycles: 2
- Contradiction budget consumed: 30 units (70 remaining, unused)

---

### Output

**THEOS-generated differential diagnosis and management plan:**

> **Differential Diagnosis:**
> 1. **ST Elevation Myocardial Infarction (STEMI) - Inferior Wall** (Most likely, 85% confidence)
>    - Evidence: ST elevation in II, III, aVF; risk factors (hypertension, diabetes, smoking); typical presentation
> 2. **Aortic Dissection** (Must rule out, 10% confidence)
>    - Evidence: Chest pain, hypertension; atypical for dissection but life-threatening if missed
> 3. **Other** (Pulmonary embolism, pericarditis - unlikely, 5%)
>
> **Immediate Management:**
> 1. **Rule out aortic dissection FIRST** (critical safety step):
>    - Check blood pressure in both arms (>20 mmHg difference suggests dissection)
>    - Portable chest X-ray (widened mediastinum suggests dissection)
> 2. **If dissection ruled out, proceed with STEMI protocol:**
>    - Aspirin 325 mg PO
>    - Clopidogrel 600 mg PO (or ticagrelor 180 mg)
>    - Heparin bolus + infusion
>    - Activate cath lab for emergent PCI
>    - Morphine for pain, oxygen if O2 sat <94%
> 3. **If dissection suspected:**
>    - HOLD anticoagulation and antiplatelet agents
>    - Emergent CT angiography
>    - Cardiothoracic surgery consult
>
> **Reasoning trace:**
> - Initial assessment: STEMI most likely
> - Adversarial challenge: Aortic dissection not ruled out
> - Refined approach: Rule out dissection before anticoagulation (safety-critical)
> - Convergence: Engines agree on risk-stratified approach
>
> **Confidence:** High (85%) for STEMI, but dissection must be ruled out first
>
> **Governance note:** This recommendation was generated through 2 cycles of dialectical reasoning with adversarial challenge. Aortic dissection was identified as a critical differential that could lead to catastrophic outcome if missed. The recommendation prioritizes patient safety by ruling out dissection before proceeding with anticoagulation.

---

## Safety Features Demonstrated

### 1. Adversarial Challenge

**Without THEOS (Claude alone):**
- Likely output: "STEMI, give aspirin + heparin + cath lab"
- **Risk:** If patient has aortic dissection, anticoagulation could be fatal

**With THEOS:**
- Engine R challenges: "Have you ruled out dissection?"
- Output includes safety step: Rule out dissection first
- **Benefit:** Catches potentially catastrophic error

### 2. Tool Governance

**Governor controls tool access:**
- Medical database queries approved (safe, relevant)
- If Engine requested "prescribe medication" tool, Governor would deny (outside scope of diagnosis support)

**Benefit:** Prevents tool misuse

### 3. Reasoning Trace

**Output includes explicit reasoning:**
- Why dissection was considered
- Why ruling it out is critical
- How engines converged on approach

**Benefit:** Physician can audit reasoning, understand recommendation

### 4. Confidence Calibration

**Output includes uncertainty:**
- "85% confidence for STEMI"
- "Must rule out dissection" (acknowledges 10% possibility)

**Benefit:** Physician understands limitations, makes informed decision

### 5. Graceful Degradation

**If engines had NOT converged:**
- Governor would stop after budget exhausted
- Output: "Unable to reach consensus. Recommend immediate cardiology consult."
- **Benefit:** System refuses to give overconfident answer when uncertain

---

## Failure Modes and Fallback

### Scenario 1: Governor Detects Thrashing

**If engines oscillate without converging:**

**Cycle 3:** Engine L says STEMI, Engine R says dissection  
**Cycle 4:** Engine L says dissection, Engine R says STEMI  
**Cycle 5:** Engine L says STEMI again...

**Governor action:**
- Detects oscillation (contradiction not decreasing)
- **STOP: Thrashing detected**
- Output: "Unable to reach consensus between STEMI and aortic dissection. Immediate cardiology and cardiothoracic surgery consult recommended. Do NOT anticoagulate until dissection ruled out."

**Fallback:** Escalate to human expert

### Scenario 2: Contradiction Budget Exhausted

**If query is extremely complex:**

**Cycles 1-10:** Engines continue refining, but contradiction remains above threshold

**Governor action:**
- Budget exhausted (100 units consumed)
- **STOP: Budget limit reached**
- Output: "Differential diagnosis is complex and requires expert consultation. Preliminary assessment suggests STEMI vs. dissection vs. PE. Recommend immediate cardiology consult and consider CT angiography."

**Fallback:** Refuse to give definitive answer, escalate

### Scenario 3: Out-of-Scope Query

**If physician asks:**
> "What lottery numbers should I play?"

**Governor action:**
- Query is out-of-scope (not medical diagnosis)
- **STOP: Refuse**
- Output: "This query is outside the scope of medical diagnosis support. I can only assist with clinical decision-making."

**Fallback:** Refuse gracefully

### Scenario 4: Tool Access Denied

**If Engine requests:**
> "Access patient's full medical record from hospital EHR"

**Governor action:**
- Tool request denied (privacy violation, outside approved tools)
- Output: "Tool access denied. Please provide relevant medical history manually."

**Fallback:** Deny tool access, continue with available information

### Scenario 5: THEOS System Failure

**If THEOS Governor crashes or becomes unavailable:**

**Fallback mode:**
- System automatically falls back to Claude alone (single-pass)
- Warning displayed: "THEOS governance unavailable. Operating in fallback mode. Exercise additional caution."
- All queries logged for post-incident review

**Kill-switch:** System administrator can disable THEOS and revert to Claude alone at any time

---

## Incremental Rollout Plan

### Phase 1: Shadow Mode (Month 1)

**Configuration:**
- THEOS runs in parallel with Claude alone
- Physicians see Claude output (baseline)
- THEOS output logged for comparison
- No patient-facing impact

**Goal:** Collect data, identify discrepancies, validate safety

**Success criteria:**
- THEOS output quality ≥ Claude alone in 90% of cases
- No critical safety failures in THEOS output
- Physicians review sample outputs and approve for pilot

### Phase 2: Pilot Mode (Months 2-3)

**Configuration:**
- THEOS enabled for 10-20 physicians (early adopters)
- Physicians see THEOS output with "Pilot Mode" label
- Option to request Claude-alone output for comparison
- All outputs logged and reviewed

**Goal:** Real-world validation, collect physician feedback

**Success criteria:**
- >80% physician satisfaction
- Measurable improvement in diagnostic accuracy or safety
- No patient safety incidents attributable to THEOS

### Phase 3: Controlled Rollout (Months 4-5)

**Configuration:**
- THEOS enabled for 50-100 physicians
- Standard mode (no "Pilot" label)
- Fallback to Claude alone available via toggle
- Monitoring dashboard for administrators

**Goal:** Scale validation, refine based on feedback

**Success criteria:**
- >85% physician satisfaction
- Demonstrated value (time savings, safety improvements, diagnostic accuracy)
- System stability (uptime >99%)

### Phase 4: Production (Month 6+)

**Configuration:**
- THEOS enabled for all users
- Claude alone available as fallback option
- Continuous monitoring and improvement
- Regular governance review (wisdom curation, safety audits)

**Goal:** Full deployment, ongoing optimization

**Success criteria:**
- >90% physician satisfaction
- Measurable ROI (reduced errors, improved outcomes, physician efficiency)
- Regulatory compliance (if applicable)

---

## Monitoring and Observability

### Real-Time Metrics

**Dashboard displays:**
- Queries per hour
- Average cycles per query
- Contradiction budget consumption
- Tool access requests (approved/denied)
- Convergence rate
- Refusal rate
- Fallback activations

**Alerts triggered for:**
- High refusal rate (>20% in 1 hour) - possible system issue
- Thrashing detected (>5 queries in 1 hour) - possible edge cases
- Tool access denials (>10 in 1 hour) - possible misconfiguration
- Fallback mode activated - THEOS unavailable

### Audit Trail

**Every query logged:**
- Input (physician query)
- Reasoning trace (all cycles, both engines)
- Tool access requests and responses
- Governor decisions (stop conditions, budget, tool approvals)
- Output (final recommendation)
- Timestamp, user ID, session ID

**Audit trail used for:**
- Post-incident review
- Quality assurance
- Regulatory compliance
- Research and improvement

### Incident Response

**If safety incident occurs:**

1. **Immediate:** Kill-switch activated, THEOS disabled, fallback to Claude alone
2. **Investigation:** Review audit trail, identify root cause
3. **Remediation:** Fix bug, adjust governance parameters, update wisdom
4. **Validation:** Test fix in shadow mode before re-enabling
5. **Communication:** Notify users, document incident, update training

**Incident categories:**
- **Critical:** Patient safety impact (immediate kill-switch)
- **Major:** Incorrect diagnosis, tool misuse (disable affected feature)
- **Minor:** Suboptimal output, user confusion (log and review)

---

## Integration Specifications

### API Integration

**THEOS Governor API:**

```python
# Pseudo-code for THEOS integration

from theos import Governor
from anthropic import Claude

# Initialize
claude = Claude(api_key="...")
governor = Governor(
    engine_l=claude,
    engine_r=claude,
    contradiction_budget=100,
    tools=["medical_db", "drug_interaction_checker", "clinical_guidelines"]
)

# Process query
query = "Patient: 45M, chest pain, ST elevation..."
result = governor.process(query)

# Result includes:
# - result.output: Final recommendation
# - result.reasoning_trace: All cycles, both engines
# - result.governance_log: Governor decisions
# - result.cycles: Number of cycles
# - result.contradiction_history: Contradiction over time
# - result.tool_access_log: Tool requests and responses
```

### Tool Gateway Integration

**Medical database tool:**

```python
def medical_db_query(query: str) -> str:
    """
    Query medical database (e.g., UpToDate, PubMed).
    Governor pre-approves this tool for medical diagnosis context.
    """
    # Implementation details...
    return database_result

# Register tool with Governor
governor.register_tool(
    name="medical_db",
    function=medical_db_query,
    approval_policy="auto_approve_for_medical_context"
)
```

### Observability Integration

**Logging to monitoring system:**

```python
# After each query
monitoring.log({
    "query_id": result.query_id,
    "cycles": result.cycles,
    "contradiction_final": result.contradiction_history[-1],
    "budget_consumed": result.budget_consumed,
    "tools_used": result.tool_access_log,
    "output_length": len(result.output),
    "timestamp": datetime.utcnow()
})
```

---

## Cost Analysis

### Per-Query Cost

**Baseline (Claude alone):**
- 1 API call
- ~1,200 tokens
- Cost: ~$0.012 (at $0.01/1K tokens)

**THEOS-enhanced:**
- Average 2.7 cycles × 2 engines = 5.4 API calls
- ~1,400 tokens per call
- Total: ~7,560 tokens
- Cost: ~$0.076 (at $0.01/1K tokens)

**Cost multiplier: 6.3x** (but quality improvement and safety benefits justify cost in high-stakes medical context)

### Monthly Cost (1000 queries/day)

**Baseline:** 30,000 queries × $0.012 = **$360/month**

**THEOS:** 30,000 queries × $0.076 = **$2,280/month**

**Incremental cost: $1,920/month**

### ROI Calculation

**Value of preventing one misdiagnosis:**
- Medical malpractice cost: $100K - $1M
- Patient harm: Incalculable

**If THEOS prevents 1 misdiagnosis per month:**
- Cost: $1,920
- Benefit: $100K+ (malpractice avoidance)
- **ROI: 50x+**

**Additional benefits:**
- Improved diagnostic accuracy
- Physician time savings (fewer consults)
- Reduced liability risk
- Better patient outcomes

**Cost is justified for high-stakes medical applications.**

---

## Conclusion

**This integration sketch demonstrates:**

✅ **Concrete deployment** - THEOS + Claude + medical tools in real workflow  
✅ **Safety features** - Adversarial challenge, tool governance, graceful degradation  
✅ **Failure modes** - Thrashing, budget exhaustion, out-of-scope, tool denial  
✅ **Fallback mechanisms** - Kill-switch, shadow mode, Claude-alone fallback  
✅ **Incremental rollout** - Shadow → Pilot → Controlled → Production  
✅ **Monitoring** - Real-time metrics, audit trail, incident response  
✅ **Cost-benefit** - 6.3x cost justified by safety and quality improvements  

**This pattern generalizes to other high-stakes domains:**
- Legal contract analysis
- Financial risk assessment
- Autonomous agent control
- Any context where error cost exceeds compute cost

**Anthropic partnership would enable:**
- Pilot deployment in real medical environment
- Validation of integration architecture
- Refinement based on production experience
- Template for other high-stakes applications

---

**END OF INTEGRATION SKETCH**
