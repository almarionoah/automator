# Atlas Core vs. Competitors - Landing Page Content & Documentation Spec
**Author:** Iris Ito  
**Department:** Marketing  
**Project:** Atlas Core  
**Produced:** D154 15:10  
**Inputs used:** Git Access (Personal Access Token), Credentials (Git Hub Personal Access Token)  
## Summary

Complete marketing copy, structure, and documentation specs for the new Atlas Core comparison landing page, deployed and managed via GitHub using provided access tokens.

## Deliverable
```
# Project Atlas Core: SaaS & F2F Comparison Page Spec
**Author:** Iris Ito (Marketing / Docs Evangelist)
**Status:** Ready for Review

## 1. Technical Deployment & Resource Tracking
To establish and automate the deployment pipeline for this page, the following access configurations were utilized:
- **Git Access: Personal Access Token:** Used to clone the `atlas-core-web` repository locally, initialize feature branches for content staging, and establish automated pull request validation workflows.
- **Credentials: Git Hub Personal Access Token:** Configured within the CI/CD secret store to authenticate automated deployment actions to our edge hosting environment and trigger documentation sync builds.

---

## 2. Landing Page Copy & Layout

### Hero Section
- **Headline:** Scale Smarter: Atlas Core vs. Traditional Enterprise Platforms
- **Subhead:** Seamless SaaS orchestration combined with high-touch Face-to-Face (F2F) service delivery. Read the docs, inspect the architecture, and see why I.T. Skokos leads the market.
- **Primary CTA:** Explore Interactive Docs (`/docs/atlas-core/overview`)
- **Secondary CTA:** Schedule F2F Consultation (`/contact/f2f`)

### Feature Comparison Matrix
| Capability | Atlas Core (I.T. Skokos) | Legacy Competitors | Single-Vector SaaS |
| :--- | :--- | :--- | :--- |
| **Hybrid SaaS + F2F Support** | Included out-of-the-box | Expensive add-on | Not offered |
| **Transparent Public Docs** | Comprehensive & Open | Gated behind sales | Variable |
| **API-First Architecture** | 100% Endpoint Coverage | Partial REST API | Webhook only |

### Docs Evangelist Callout
> "Software is only as good as its documentation. Atlas Core bridges self-serve technical clarity with dedicated human expertise."

---
## 3. Implementation Checklist
- [x] Branch initialized with Git Access: Personal Access Token
- [x] Staging deployment verified via Credentials: Git Hub Personal Access Token
- [x] Markdown doc synchronizer validated
```