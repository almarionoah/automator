# Beacon API Competitor Comparison Landing Page Specification & Tracking Matrix
**Author:** Juno Hale  
**Department:** Marketing  
**Project:** Beacon API  
**Produced:** D15 10:50  
**Inputs used:** Business Document (Company Document)  
## Summary

Data-backed comparison landing page copy, empirical benchmark table, and telemetry tracking schema for Beacon API, utilizing verified metrics from Company Document.

## Deliverable
```
# Specification: Beacon API vs. Legacy Gateways (Landing Page & Telemetry Matrix)
**Author:** Juno Hale | Marketing (Data Purist)
**Project:** Beacon API
**Reference Resource:** `Company Document`

---
### 1. Data Validation & Resource Utilization
- **Company Document Application:** Sourced verified enterprise benchmarks, tier limits, and SLA uptime guarantees (99.99%) from `Company Document` to eliminate subjective marketing claims and ground all comparison vectors in empirical performance data (latency, request pricing, and hybrid face-to-face onboarding SLAs).

### 2. Page Structure & Quantitative Copy Matrix

#### Hero Section
- **H1:** Real-Time Ingestion Without Legacy Overhead
- **Subhead:** Beacon API processes sub-15ms payload deliveries at 42% lower cost per 1M requests compared to standard REST brokers.
- **Primary CTA:** Start Free 50k Event Baseline Test (`btn_primary_trial`)
- **Secondary CTA:** Book Face-to-Face Technical Scoping Session (`btn_secondary_f2f`)

#### Quantitative Performance Grid
| Dimension | Beacon API | Gateway Alpha | CloudSync Pro |
| :--- | :--- | :--- | :--- |
| **p99 Ingestion Latency** | **14.2 ms** (Verified) | 88.6 ms | 46.1 ms |
| **Compute Cost / 1M Requests** | **$1.80** | $3.90 | $3.10 |
| **Deployment Model** | Hybrid SaaS + F2F Support | Multi-tenant Only | Cloud Only |
| **SLA Backing** | 99.99% Financial Credit | 99.9% Best Effort | 99.95% |

### 3. Telemetry & Experimentation Framework
- **Primary Metric:** Trial Sign-up Conversion Rate (Target: 4.85%, p-value < 0.01).
- **Event Tracking Schema:**
  - `lp_comparison_view`: Viewport >= 50% duration > 3.0s.
  - `lp_benchmark_interaction`: Filter/toggle switch between SaaS vs Hybrid F2F tiers.
  - `lp_conversion_submit`: Captures payload: `{ tier_selected, attribution_source, estimated_monthly_req }`.
```