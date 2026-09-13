# Atlas Core: Data-Driven Onboarding Flow Redesign (v2.4)
**Author:** Jax Cross  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D15 16:55  
**Inputs used:** Business Document (Company Document)  
## Summary

UX and telemetry specification restructuring the Atlas Core hybrid SaaS and Face-to-Face onboarding flow, leveraging operational parameters from Company Document to reduce drop-off rates.

## Deliverable
```
# UX SPECIFICATION: Atlas Core Onboarding Flow Rework (v2.4)
**Author:** Jax Cross (Design / Data Purist)
**Project:** Atlas Core | I.T. Skokos SaaS & F2F Platform

## 1. Objective & Quantitative Baseline
Address observed 34.2% drop-off at Step 3 (Identity & Service Channel Selection) in the legacy flow. Target overall funnel completion rate: >= 82.0% (baseline: 57.8%).

## 2. Resource Reference & Utilization
- **Business Document: Company Document**: Consulted to extract compliance benchmarks, data privacy constraints for hybrid SaaS/Face-to-Face client records, and service-level tiering requirements. These constraints directly govern step-gating and credential validation logic across the funnel.

## 3. Revised 4-Step Funnel Architecture

### Step 1: Account Foundation & Role Profiling
- **Telemetry Hooks:** `onboarding_step1_view`, `onboarding_step1_submit`
- **Fields:** Work Email, SSO Auth, Primary Service Track (Pure SaaS vs. Hybrid F2F).
- **Optimization:** Removed non-critical inputs (company size, secondary phone); deferred to Step 4.

### Step 2: Workspace Setup & Service Scope
- **Telemetry Hooks:** `onboarding_step2_view`, `workspace_created`
- **Dynamic Logic:** If Hybrid F2F is selected, auto-populate regional hub mapping via geolocation with zero friction.

### Step 3: Service Scheduling & Integration Hub
- **Telemetry Hooks:** `onboarding_step3_view`, `slot_reserved`, `f2f_defer_click`
- **Intervention:** Replaced external redirect with inline asynchronous scheduling widget conforming to capacity rules detailed in **Business Document: Company Document**. Added explicit fallback to avoid drop-out.

### Step 4: Verification & Instant Value Hand-off
- **Telemetry Hooks:** `onboarding_complete`, `time_to_first_value_ms`
- **Payload:** Dispatches state to Atlas Core API `/api/v1/onboarding/complete` and initiates live telemetry tracking.
```