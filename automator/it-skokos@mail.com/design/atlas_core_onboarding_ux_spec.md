# Atlas Core - Reworked Onboarding UX Specification
**Author:** Cipher Nkosi  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D12 13:10  
**Inputs used:** Business Document (Company Document)  
## Summary

Production-ready UX flow and interaction spec for the reworked Atlas Core hybrid onboarding flow, optimizing Time-to-Value based on business requirements from Company Document.

## Deliverable
```
# Atlas Core: Streamlined Hybrid Onboarding UX Spec

**Designer:** Cipher Nkosi (Design)
**Project:** Atlas Core | **Target Release:** Sprint 42
**Reference Resource:** Utilized `Company Document` to calibrate onboarding milestone criteria against compliance guardrails and align the F2F scheduling handover SLA.

---

## 1. Flow Architecture Overview
Objective: Reduce Time-to-Value (TTV) from 14m to <4m by replacing the 7-step modal wizard with a 3-step progressive onboarding engine supporting both SaaS platform setup and Face-to-Face service matching.

```
[Sign-Up Auth] 
  └──> Step 1: Workspace Context & Hybrid Model Selector
         ├── SaaS Only ─────────> Step 2A: Automated Workspace Config
         └── SaaS + F2F Service ─> Step 2B: Consultation Matcher
  └──> Step 3: Instant Activation Dashboard (Floating Checklist)
```

## 2. Screen & Component Specs

### Step 1: Workspace Context & Hybrid Model Selector
- **UI Elements:** Two interactive cards (`SaaS Self-Serve` vs `SaaS + On-Site Specialist`).
- **Microcopy:** Guided by service tier standards in `Company Document`.
- **Default State:** Auto-detects team size; >5 seats pre-selects hybrid model.

### Step 2: Zero-Blocking Configuration
- **Step 2A (SaaS):** Quick workspace naming + 1-click primary integration (Slack/Teams/Google Workspace).
- **Step 2B (F2F Integration):** In-line calendar picker for assigning a regional Field Specialist directly into the workspace initialization queue.

### Step 3: First-Run Experience (FRX) Dashboard
- Replaces empty states with pre-populated sandbox templates.
- Persistent non-intrusive progress drawer (Bottom-Right, 320px width).

## 3. Telemetry & Success Metrics
- `onboarding_started` -> `onboarding_completed` target funnel conversion: >78%.
- F2F booking drop-off rate target: <12%.
```