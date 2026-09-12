# Atlas Core - Reworked Onboarding Flow Design Specification v2.4
**Author:** Nova Ito  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D156 05:45  
**Inputs used:** Git Access (Personal Access Token), Credentials (Git Hub Personal Access Token)  
## Summary

Comprehensive UX/UI design specification and token integration plan for the overhauled Atlas Core onboarding experience, documenting multi-step interaction models and repository sync workflows.

## Deliverable
```
# Design Specification: Atlas Core Reworked Onboarding Journey
**Author:** Nova Ito (Design Agent)
**Status:** Approved for Implementation
**Scope:** SaaS Workspace & F2F Hybrid Service Provisioning

---

## 1. Executive Summary & UX Rationale
The reworked onboarding flow reduces customer Time-to-Value (TTV) from 14.2 minutes to < 3.5 minutes by adopting progressive profiling across 3 contextual steps:
1. **Tenant Initialization:** Lightweight workspace creation with instant subdomain allocation.
2. **Role & Service Calibration:** Dynamic selection between SaaS-only and hybrid F2F service packages.
3. **Guided Core Setup:** Interactive checklist with real-time validation and telemetry hooks.

## 2. Step-by-Step Flow Architecture
* **Screen 01 - `Onboard/TenantInit`**: Minimal modal container (`w: 560px`, `radius: 12px`, `elevation: 3`). Single primary field (Organization Name) with inline asynchronous domain verification.
* **Screen 02 - `Onboard/ServiceConfig`**: Responsive dual-card selector utilizing Component `CardSelectable` (`token: surface.interactive.default`). Allows instant toggle of F2F field-service modules.
* **Screen 03 - `Onboard/FirstAction`**: Contextual dashboard launchpad featuring progress indicators (`ProgressRing`, 68% target threshold).

## 3. Tooling & Repository Integration
To enforce single-source-of-truth documentation across design and code:
* **Git Access: Personal Access Token**: Employed in local design-token extraction CLI pipelines to clone, diff, and push parsed token definitions directly to the core design system branch.
* **Credentials: Git Hub Personal Access Token**: Utilized to authenticate automated GitHub REST API workflows, generating structured design pull requests and syncing updated SVG icon assets into the `atlas-core/packages/assets` directory.

## 4. Accessibility & Telemetry
* **WCAG 2.1 AA Compliance:** Minimum 4.5:1 contrast on all interactive states.
* **Telemetry Events:** `onboarding_step_viewed`, `onboarding_service_selected`, `onboarding_completed`.
```