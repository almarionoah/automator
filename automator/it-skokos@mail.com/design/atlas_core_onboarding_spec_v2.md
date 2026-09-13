# Atlas Core - Reworked Onboarding Flow & Edge-Case UX Specification
**Author:** Byte Hale  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D17 01:25  
**Inputs used:** Business Document (Company Document)  
## Summary

Comprehensive UX design specification for the reworked Atlas Core onboarding flow, mapping primary user journeys, critical edge-case recovery paths, and alignment with baseline requirements from Company Document.

## Deliverable
```
# UX Design Specification: Atlas Core Onboarding Redesign (v2.0)
**Author:** Byte Hale (Design Agent) | **Project:** Atlas Core
**Reference Resource:** *Company Document* (utilized for baseline operational requirements, regulatory compliance checkpoints, and hybrid SaaS/Face-to-Face handover rules).

---

## 1. Context & Objective
The Atlas Core onboarding workflow required restructuring to eliminate friction between digital SaaS provisioning and physical face-to-face scheduling, while hardening edge cases that historically caused drop-offs.

## 2. Document Alignment
- **Company Document**: Consulted to establish mandatory KYC/verification steps, SLA commitments for face-to-face service dispatch, and user permission boundaries across tenant tiers.

## 3. Flow Architecture & State Machine

```
[Start] -> [Account Setup] -> [Role & Scope Definition] 
        -> [Service Routing Matrix]
             ├─> SaaS-only Path -> [Self-Guided Workspace Provisioning] -> [Done]
             └─> Hybrid Path   -> [Face-to-Face Consult Scheduler]   -> [Telemetry Sync] -> [Done]
```

## 4. Edge-Case Archeology & Mitigation Matrices

| Edge Case ID | Scenario | Fallback & UI State |
|---|---|---|
| **EC-01: Split-Tenant Latency** | User switches organization domain mid-invite session. | Enforce atomic session invalidation; render non-blocking modal with preserved input state. |
| **EC-02: Geo-Fencing Mismatch** | Face-to-Face service selected in unserviced region (per *Company Document* matrix). | Auto-fallback to remote setup with inline calendar override and priority queue badge. |
| **EC-03: Partial Token Drop** | Third-party auth provider returns null email scope during MFA. | Route to explicit scope remediation step without restarting flow. |

## 5. Next Steps
- Sync design tokens with frontend repo (`@atlas/ui-core`).
- Deliver interactive Figma state prototypes to QA.
```