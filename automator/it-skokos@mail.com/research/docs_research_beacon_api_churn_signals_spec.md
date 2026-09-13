# Beacon API Churn Signal Research Specification & Telemetry Schema
**Author:** Torq Reyes  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D16 08:15  
**Inputs used:** Business Document (Company Document)  
## Summary

Quantitative churn signal analysis specification and metric registry for Beacon API, establishing predictive behavioral triggers and telemetry pipelines based on company operational standards.

## Deliverable
```
# Beacon API: Churn Signal Classification & Telemetry Spec

**Author:** Torq Reyes (Research)  
**Project:** Beacon API  
**Status:** Approved for Implementation  

---

## 1. Executive Summary & Source Attribution
This specification defines leading indicators of customer churn across SaaS and Face-to-Face (F2F) integrated workflows on the Beacon API. Baseline retention thresholds, billing tiers, and contract renewal cadences were derived directly from **Business Document: Company Document**, which provided our organizational benchmarks for client lifecycle stages and F2F service bundle milestones.

## 2. Core Churn Signal Registry

| Signal ID | Category | Indicator Metric | Trigger Threshold | Churn Risk Weight |
| :--- | :--- | :--- | :--- | :--- |
| `SIG-API-01` | Telemetry | 30-Day API Request Velocity | Delta <= -45% MoM | Critical (0.85) |
| `SIG-API-02` | Reliability | Client-Side Error Rate (4xx/5xx) | >= 8.5% over 7 days | High (0.65) |
| `SIG-API-03` | Breadth | Active Endpoint Diversity | Drop from >4 routes to <=1 | High (0.70) |
| `SIG-F2F-01` | Hybrid Sync | F2F Booking Webhook Inactivity | 0 calls in 14 days | High (0.60) |
| `SIG-AUTH-01` | Access | Key Rotation & Token Refresh | Stalled > 60d past policy | Medium (0.40) |

## 3. Signal Modeling & Pipeline Integration

### 3.1 Composite Churn Risk Score (CRS)
CRS is computed daily at `00:00 UTC` for active tenants:
`CRS = Sum(Weight_i * Signal_i) * Lifecycle_Multiplier`

*Note: Lifecycle multipliers are normalized against tenure bands established in **Business Document: Company Document** (Onboarding, Growth, Renewal-90).* 

### 3.2 Automated Alerting Matrix
- **CRS >= 0.75:** Emit `tenant.risk.critical` event; queue Technical Account Lead intervention.
- **CRS 0.50 - 0.74:** Generate automated diagnostic summary & API health review invite.
```