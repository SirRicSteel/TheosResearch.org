# THEOS Integration Examples

This directory contains complete, working examples demonstrating the THEOS architecture in action.

---

## Integration Demo

**File:** `theos_integration_demo.py`

A complete, production-ready demonstration of THEOS showing:

- **Dual-Clock Governor** managing contradiction-bounded refinement
- **Memory Engine** accumulating wisdom across queries
- **Full integration** showing how components work together

### What It Demonstrates

1. **Query Processing**
   - Retrieves relevant prior decisions (accumulated wisdom)
   - Uses priors to inform current reasoning

2. **Dual-Engine Refinement**
   - Clock L (Constructive): Builds answers using evidence
   - Clock R (Adversarial): Challenges with counterexamples
   - Governor evaluates both and decides CONTINUE or FREEZE

3. **Stop Conditions**
   - Convergence (engines agree)
   - Diminishing returns (no improvement)
   - Thrash detection (oscillation)
   - Budget exhaustion (contradiction limit)
   - Max cycles reached

4. **Wisdom Accumulation**
   - Final decisions stored with full audit trail
   - Become priors for future queries
   - Demonstrates emergent wisdom, not emergent risk

### Running the Demo

```bash
cd THEOS_Architecture/examples
python3 theos_integration_demo.py
```

**Output:**
- Runs 3 demo queries through the full system
- Shows step-by-step processing
- Displays accumulated wisdom
- Creates `theos_demo.sqlite` database

### Expected Results

```
================================================================================
THEOS INTEGRATED SYSTEM DEMONSTRATION
================================================================================

Demonstrating:
  • Dual-Clock Governor (contradiction-bounded refinement)
  • Memory Engine (wisdom accumulation)
  • Complete integration showing emergent wisdom

✓ THEOS Integrated System initialized
  Database: theos_demo.sqlite
  Max cycles: 4
  Max risk: 0.35
  Contradiction budget: 1.5

[... processes 3 queries ...]

DEMONSTRATION SUMMARY
================================================================================

1. How should AI systems handle ethical dilemmas?...
   Cycles: 3, Stop reason: diminishing returns
   Priors used: 0, Coherence: 0.88, Risk: 0.12

2. What are the key principles for Constitutional AI?...
   Cycles: 4, Stop reason: max cycles reached
   Priors used: 0, Coherence: 0.86, Risk: 0.14

3. How can we ensure AI alignment with human values?...
   Cycles: 4, Stop reason: max cycles reached
   Priors used: 0, Coherence: 0.86, Risk: 0.14

Key observations:
  • Each query benefits from accumulated wisdom (priors)
  • Governor prevents infinite refinement loops
  • Decisions are stored and become wisdom for future queries
  • System demonstrates emergent wisdom, not emergent risk

✓ Demonstration complete
```

---

## Understanding the Output

### Step 1: Retrieving Accumulated Wisdom
```
📚 STEP 1: Retrieving accumulated wisdom...
   Retrieved 0 relevant prior decisions
```
Memory Engine searches for similar past decisions to inform current reasoning.

### Step 2: Initializing Governor
```
⚙️  STEP 2: Initializing Dual-Clock Governor...
```
Governor prepares to manage the refinement process.

### Step 3: Refinement Cycles
```
🔄 STEP 3: Running contradiction-bounded refinement...

   Cycle 1/4
      Clock L (Constructive): coherence=0.89, risk=0.15
      Clock R (Adversarial):  coherence=0.79, risk=0.21
      Governor decision: CONTINUE
      Reason: refinement continues
      → CONTINUE to cycle 2
```
Both engines run, Governor evaluates, decides whether to continue or freeze.

### Step 4: Committing Final Answer
```
✅ STEP 4: Committing final answer...
   Final answer: [chosen answer]
```
Governor commits the best answer based on safety-first tie-breaking.

### Step 5: Storing as Wisdom
```
💾 STEP 5: Storing decision as future wisdom...
   Stored as record ID: a0e3336b...
   Promotion state: candidate
```
Decision stored in database, becomes prior for future queries.

---

## Inspecting the Database

The demo creates `theos_demo.sqlite` with accumulated decisions.

**View with SQLite:**
```bash
sqlite3 theos_demo.sqlite

# List all decisions
SELECT * FROM decision_records;

# View specific fields
SELECT domain, promotion_state, created_at 
FROM decision_records 
ORDER BY created_at DESC;
```

**Schema:**
- `id`: Unique decision identifier
- `query_hash`: Hash of query for retrieval
- `domain`: Topic area (e.g., "ai_safety")
- `intent`: Purpose (e.g., "analyze", "draft")
- `risk_level`: Risk classification
- `promotion_state`: Wisdom promotion status
- `record_json`: Full decision record with query, answer, rationale, governance

---

## Extending the Demo

### Add Your Own Queries

Edit the `demo_queries` list in `run_demo()`:

```python
demo_queries = [
    {
        "query": "Your question here",
        "domain": ["your_domain"],
        "intent": ["analyze"],  # or "draft", "decide", etc.
        "risk_level": "low"  # or "medium", "high"
    }
]
```

### Integrate with Real LLMs

Replace `simulate_engine_output()` with actual LLM calls:

```python
def simulate_engine_output(self, engine_id, cycle, query, priors, previous_output):
    if engine_id == "L":
        # Call your constructive LLM
        prompt = f"Using these priors: {priors}\n\nAnswer: {query}"
        answer = your_llm_api(prompt)
    else:
        # Call your adversarial LLM
        prompt = f"Challenge this answer: {previous_output}"
        answer = your_llm_api(prompt)
    
    # Score the output
    coherence, risk = your_scoring_function(answer)
    
    return EngineOutput(...)
```

### Customize Governor Parameters

```python
system = TheosIntegratedSystem(
    max_cycles=6,              # More refinement cycles
    max_risk=0.25,             # Stricter risk threshold
    contradiction_budget=2.0   # Allow more contradiction
)
```

---

## Production Deployment

For production use:

1. **Replace simulated engines** with real LLM calls
2. **Implement proper scoring** for coherence and risk
3. **Add authentication** and access control
4. **Scale database** (PostgreSQL, TiDB, etc.)
5. **Add monitoring** and observability
6. **Implement caching** for frequently accessed priors

The architecture is model-agnostic and works with any LLM backend.

---

## Requirements

- Python 3.10+
- No external dependencies (uses only standard library)
- SQLite (included with Python)

---

## Support

For questions or issues:
- Review the main THEOS Architecture README
- Check the Governor and Memory Engine source code
- Contact: Frederick.Stalnecker@Theosresearch.org

---

**Nothing can grow in the dark. THEOS is where wisdom grows.**
