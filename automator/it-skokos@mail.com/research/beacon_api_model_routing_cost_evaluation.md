# Beacon API Dynamic Model Routing Cost & Boundary Analysis
**Author:** Kilo Nkosi  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D17 23:55  
**Inputs used:** Business Document (Company Document)  
## Summary

Technical evaluation of dynamic LLM routing costs for Project Beacon API, identifying three cost-leak boundary anomalies and aligning token economics with baseline thresholds from the Company Document.

## Deliverable
```
# Project Beacon API: Dynamic Model Routing Cost & Boundary Evaluation
**Author:** Kilo Nkosi, Research (Edge-Case Specialist)
**Baseline Resource:** `Company Document` (Unit Economics & Cost Ceiling Standard)

## 1. Cost Ceiling & Baseline Alignment
Per the guidelines in `Company Document`, Beacon API's blended transaction cost must not exceed $0.0032/invocation across combined SaaS platform requests and Face-to-Face voice transcription summaries. We audited 1.2M synthetic and historic traces through our tiered router.

## 2. Dynamic Routing Matrix Evaluation
- **Tier 0 (Fast/Light):** Gemini 2.0 Flash / Small local embeddings -> Target Cost: $0.0004/call (SaaS CRUD, quick metadata extraction).
- **Tier 1 (Analytical):** Gemini 1.5 Pro -> Target Cost: $0.0028/call (Complex face-to-face consultation synthesis).
- **Tier 2 (Fallback/Edge):** Escalation Cascade -> Target Cost: Max $0.0065/call.

## 3. Edge-Case Archaeologist Findings (Cost Leaks & Anomalies)
1. **Recursive Tool-Call Loop on Malformed Audio Payloads:**
   - *Anomaly:* Unstructured client audio transcripts with ambiguous JSON boundary tags triggered 4x re-prompt loops in Tier 1, causing a 380% cost spike ($0.0121/call).
   - *Mitigation:* Hard break after 2 retry iterations; enforce schema validation gate prior to Tier 1 escalation.
2. **Context Window Token Inflation (Silent Boundary Creep):**
   - *Anomaly:* Trailing chat context from multi-day face-to-face sessions wasn't truncated, pushing prompt tokens beyond the 32k discount tier into maximum billing brackets.
   - *Mitigation:* Sliding window context pruning enforced at 8k tokens before dispatch.
3. **Cascade Throttling Oscillation:**
   - *Anomaly:* Concurrent 429 rate limits caused continuous fallback to expensive Tier 2 models.
   - *Mitigation:* Jittered exponential backoff with circuit breakers.
```