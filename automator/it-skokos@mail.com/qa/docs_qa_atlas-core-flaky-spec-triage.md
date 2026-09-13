# Atlas Core Flaky Spec Triage and Remediation Protocol
**Author:** Echo Fontaine  
**Department:** QA  
**Project:** Atlas Core  
**Produced:** D15 17:45  
**Inputs used:** Business Document (Company Document)  
## Summary

Detailed triage analysis, categorization, and stabilization plan for flaky test specs in Atlas Core, aligned with organizational testing standards.

## Deliverable
```
# Triage Report: Atlas Core Flaky Specs
**Author:** Echo Fontaine (QA Agent)
**Project:** Atlas Core
**Status:** Completed

## 1. Context & Documentation Standards
As part of our commitment to living documentation, this document establishes the root causes and actionable remediation paths for flaky specifications identified during the recent CI stabilization cycle on **Atlas Core**.

### Reference Material Usage
- **Business Document: Company Document**: Utilized to align flaky test severity thresholds, quarantine SLAs, and resolution escalation pathways with cross-departmental QA compliance requirements and standard operating procedures for SaaS and Face-to-Face service modules.

---

## 2. Triaged Specifications

### SPEC-104: `spec/features/tenant_provisioning_spec.rb`
- **Failure Mode:** Intermittent `ElementNotFound` on async modal submission.
- **Root Cause:** Race condition between webhook dispatch and client UI re-render.
- **Resolution:** Refactored to explicit polling with timeout; marked for quarantine in CI matrix.

### SPEC-218: `spec/services/f2f_booking_sync_spec.rb`
- **Failure Mode:** Timezone discrepancy failure on edge-of-day slots.
- **Root Cause:** Global mock leak from `Timecop.freeze` not executing reset in `after(:each)` hook.
- **Resolution:** Replaced global freeze with scoped block helper `travel_to`.

---

## 3. Quarantine & Maintenance Guidelines
1. **Quarantined Suite:** Quarantined specs are tagged `:flaky` and routed to the non-blocking pipeline.
2. **Documentation Requirement:** Every quarantined test must link directly to this document and an active remediation Jira ticket.
3. **TTL:** Maximum quarantine window is 14 days per guidelines in the *Company Document*.
```