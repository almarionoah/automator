# Atlas Core - Streamlined Hybrid Onboarding Spec
**Author:** Volt Reyes  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D11 09:00  
**Inputs used:** Business Document (Company Document)  
## Summary

Pragmatic 3-step onboarding flow spec for Atlas Core, aligning SaaS self-serve with Face-to-Face concierge service handoffs.

## Deliverable
```
# Atlas Core: Reworked Onboarding Flow Specification
**Owner:** Volt Reyes (Design)
**Project:** Atlas Core
**Status:** Ready for Engineering Hand-off

## 1. Context & Business Alignment
Per guidance from the **Company Document**, our onboarding flow previously suffered a 34% drop-off due to early high-friction data entry. Using the compliance and service delivery parameters defined in **Company Document**, this rework decouples initial SaaS workspace creation from the Face-to-Face service configuration, allowing immediate time-to-value while capturing booking intent.

---

## 2. 3-Step Flow Architecture

### Step 1: Account Context & Service Tier Selection
- **Route:** `/onboarding/step-1`
- **UI Components:**
  - `WorkspaceInput` (autofills slug)
  - `ServiceModeRadioGroup`: [SaaS Self-Serve | Hybrid SaaS + Face-to-Face Concierge]
- **Validation:** Workspace name required (>3 chars). Default selection defaults to Hybrid per **Company Document** go-to-market targets.

### Step 2: Quick Configuration & Team Invites
- **Route:** `/onboarding/step-2`
- **UI Components:**
  - `RoleMultiSelect` (Admin, Operator, Field Specialist)
  - `InvitePillInput` (Max 5 inline invites; remainder deferred to workspace settings)
- **Action:** Skip option clearly visible (`variant="tertiary"`, no blocking modal).

### Step 3: Activation Handoff
- **Route:** `/onboarding/step-3`
- **Conditional Render:**
  - *If SaaS Self-Serve:* Render `InstantDashboardRedirect` with quickstart checklist modal.
  - *If Hybrid:* Render `ConciergeSchedulerCard` (Cal.com embedded widget for Face-to-Face intake session) + primary CTA "Complete Later in Dashboard".

---

## 3. Telemetry & Success Metrics
- Track `onboarding_started`, `step_completed`, `f2f_scheduled`, `onboarding_completed`.
- Target completion time: < 90 seconds (reduced from 4.5 minutes).
```