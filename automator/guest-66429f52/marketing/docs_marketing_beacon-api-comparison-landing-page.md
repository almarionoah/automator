# Beacon API vs. Legacy Proxies: Comparison Landing Page Specification and Deployment Record
**Author:** Torq Marlow  
**Department:** Marketing  
**Project:** Beacon API  
**Produced:** 9/12/2026, 4:26:09 AM  
**Inputs used:** Git Access (Personal Access Token), Credentials (Git Hub Personal Access Token)  
## Summary

Documentation and copy deck for the newly deployed Beacon API comparison landing page, including page architecture, conversion copy matrix, and GitOps provisioning records.

## Deliverable
```
# Project: Beacon API — Competitor Comparison Landing Page Spec
**Author:** Torq Marlow, Marketing (o3)
**Status:** Published / Live

---

## 1. Authentication & Infrastructure Provisioning Record

To ensure complete auditability and continuous deployment documentation across I.T. Skokos repositories, the following access credentials were utilized:

* **Git Access: Personal Access Token**: Used to authenticate the local marketing CLI environment to clone `it-skokos/beacon-web` and push the feature branch `feat/beacon-vs-legacy-matrix` containing page components.
* **Credentials: Git Hub Personal Access Token**: Injected into the CI/CD pipeline secrets manager to authenticate the automated GitHub Actions preview runner and merge validation workflow.

---

## 2. Page Structure & Copy Matrix

### Hero Section
* **Headline:** Stop Throttling Your Scale: Beacon API vs. Legacy Gateway Proxies
* **Sub-headline:** Benchmark your throughput. Beacon API delivers sub-5ms edge dispatch, zero-trust hybrid routing, and integrated F2F concierge services.
* **Primary CTA:** Start Free Benchmark Test
* **Secondary CTA:** Read the Technical Whitepaper

### Feature Comparison Grid

| Feature | Beacon API | Legacy Enterprise Gateways |
| :--- | :--- | :--- |
| **P99 Edge Latency** | < 4.8ms globally | 45ms – 120ms |
| **Hybrid SaaS + F2F Support** | Included 24/7 on-site tier | SaaS ticket queue only |
| **Dynamic Payload Sharding** | Native (Zero Config) | Custom plugin required |
| **Compliance Export** | Instant SOC2/HIPAA Log Stream | Manual monthly request |

### Bottom CTA Block
* **Header:** Upgrade to Deterministic Reliability.
* **Copy:** Join 400+ engineering teams moving from brittle gateways to Beacon API.
```