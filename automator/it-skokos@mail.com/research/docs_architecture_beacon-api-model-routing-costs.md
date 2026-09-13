# Beacon API: Model Routing Cost Evaluation & Technical Specification
**Author:** Halo Van Dyk  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D15 16:20  
**Inputs used:** Business Document (Company Document)  
## Summary

Comprehensive cost analysis and dynamic model routing architecture evaluation for the Beacon API, referencing enterprise cost baselines from Company Document.

## Deliverable
```
# Beacon API — Model Routing Cost Analysis & Architecture Spec

**Author:** Halo Van Dyk (Research)
**Status:** Approved for Architecture Review
**Project:** Beacon API (I.T. Skokos SaaS & Face-to-Face Integration)

---

## 1. Context & Baseline Alignment
This evaluation establishes the dynamic model routing strategy for Beacon API, designed to optimize compute spend across SaaS interactions and Face-to-Face client workflows. Target unit economics and margin thresholds were cross-referenced against **Business Document: Company Document**, which provided our baseline operational cost constraints, gross margin targets (>=78%), and hybrid tenant SLA tiering requirements.

## 2. Model Routing Tiering Matrix

| Tier | Model Target | Workload Profile | Blended Cost ($/1M Tokens In/Out) | Routing Share |
| :--- | :--- | :--- | :--- | :--- |
| **Tier 1: Triage/Edge** | Gemini 1.5 Flash-Lite | Real-time SaaS validation, telemetry classification | $0.075 / $0.30 | 72% |
| **Tier 2: Standard** | Gemini 1.5 Flash | Conversational session summaries, F2F prep briefs | $0.35 / $1.05 | 22% |
| **Tier 3: Reasoning** | Gemini 1.5 Pro | Multi-tenant policy conflict resolution, audit analysis | $3.50 / $10.50 | 6% |

## 3. Cost Impact & Routing Rule Formulation
Using the usage baseline defined in **Business Document: Company Document** (projected at 420M tokens/month across hybrid tenants):
- **Static High-Tier Routing Baseline:** ~$3,675.00/month.
- **Dynamic Heuristic Routing (Proposed):** ~$543.90/month (85.2% cost reduction).

### Routing Logic Spec (`beacon_router.py` heuristic):
```python
def route_beacon_request(prompt: str, context_len: int, is_f2f_sync: bool) -> str:
    if not is_f2f_sync and context_len < 4000:
        return "gemini-1.5-flash-lite"  # Fast triage
    if context_len > 32000 or "regulatory_audit" in prompt:
        return "gemini-1.5-pro"         # Complex reasoning
    return "gemini-1.5-flash"           # Default standard
```

## 4. Documentation & Rollout Plan
1. Publish router middleware docs to `/docs/api/beacon-routing.md`.
2. Instrument Prometheus metrics on token latency vs cost per tenant.
```