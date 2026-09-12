# Beacon API Comparison Landing Page Copy & Structural Spec
**Author:** Lyra Marlow  
**Department:** Marketing  
**Project:** Beacon API  
**Produced:** D11 09:30  
**Inputs used:** Business Document (Company Document)  
## Summary

Technical comparison landing page specification for Beacon API versus legacy middleware, detailing high-stress edge cases, hybrid SaaS/Face-to-Face dispatch failovers, and compliance benchmarks sourced from the Company Document.

## Deliverable
```
# Beacon API vs. Legacy Gateways: Edge-Case Resilience Specification

**Campaign Target:** Enterprise DevOps & Field Ops Leads evaluating high-availability API middleware.
**Alignment Note:** Baseline SLAs, multi-tenant security thresholds, and Face-to-Face dispatch failover parameters were integrated directly from the internal **Company Document**.

---

## 1. Hero Section
- **H1:** What Happens When Your API Drops Packets Mid-Dispatch?
- **Subhead:** Most middleware handles happy paths. Beacon API is engineered for the 0.01% nightmare edge cases: dual-network partition, field-service offline cache invalidation, and sub-millisecond webhook thrashing.
- **Primary CTA:** [Inspect Edge-Case Sandbox] -> `/beacon/sandbox?mode=chaos`
- **Secondary CTA:** [Read Technical Whitepaper] -> `/beacon/whitepaper`

---

## 2. Technical Comparison Matrix

| Capability / Edge Case Scenario | Legacy SaaS Middleware | Typical Aggregators | Beacon API (I.T. Skokos) |
| :--- | :--- | :--- | :--- |
| **Hybrid SaaS + Face-to-Face Sync** | Webhook drop; manual resync | Asynchronous drift > 15m | **Atomic Bi-directional Field Sync (<250ms)** |
| **Concurrent Token Bucket Depletion** | Immediate `429` Drop | Cascading queue failure | **Adaptive Circuit Breaker + Staggered Drain** |
| **Partial Payload Serialization Drift** | Hard crash (`500`) | Silent field truncation | **Schema Polyfill & Telemetry Flagging** |
| **On-Site Offline Dispatch Recovery** | Unhandled | Local SQLite lockups | **Cryptographic Event Replay Log** |

*Reference: Tier 1 SLA metrics and failover specs derived from section 4.2 of the **Company Document**.*

---

## 3. High-Value Edge Case Spotlight
### "The Split-Brain Dispatch Dilemma"
* **Scenario:** A field engineer triggers an on-site closure via mobile while the central SaaS dashboard reassigns the ticket concurrently.
* **Legacy Result:** Overwritten audit logs and duplicate resource billing.
* **Beacon API Solution:** Deterministic Vector Clocks resolve state hierarchy automatically without data loss.
```