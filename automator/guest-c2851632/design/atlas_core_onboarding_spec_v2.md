# Atlas Core Onboarding Flow Redesign Specification
**Author:** Quill Petrov  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D6 15:45  
**Inputs used:** Business Document (Company Document)  
## Summary

Comprehensive UX design specification addressing edge-case states, progressive profiling, and hybrid SaaS/in-person service transitions for Atlas Core onboarding.

## Deliverable
```
# UX Design Spec: Atlas Core Reworked Onboarding Flow
Author: Quill Petrov (Design)
Project: Atlas Core
Status: Ready for Review

## 1. Overview & Context
This specification redesigns the Atlas Core onboarding journey to address drop-offs identified during hybrid SaaS and Face-to-Face transitions. In accordance with the foundational guidelines in 'Business Document: Company Document', this flow enforces strict compliance checks, identity validation tiers, and service-readiness metrics before granting platform provisioning.

## 2. Resource Utilization
- **Business Document: Company Document**: Utilized to align step-by-step identity verification mandates with internal operational policies, specifically mapping required user consent screens and SLA expectations for Face to Face onboarding booking.

## 3. Edge-Case Mapping & Architecture

### Step 1: Initial Profile & Org Structure
- Primary: Email auth -> Role selection -> Workspace provisioning.
- Edge Case 1.1 (Multi-domain invites): Detect pending enterprise domain invites; present seamless merge prompt without session invalidation.
- Edge Case 1.2 (Throttled verification): Inline retry mechanism with exponential backoff visual indicator.

### Step 2: Hybrid Service Qualification (Face to Face)
- Primary: Assessment of SaaS-only vs. In-Person concierge requirements.
- Edge Case 2.1 (Unsupported Geo): Fallback to remote concierge flow; persist selected parameters without data loss.
- Edge Case 2.2 (Calendar Sync Disconnect): Asynchronous booking hold allowing completion of SaaS setup while reserving a 24h tentative slot.

### Step 3: Workspace Config & Role-Based Permissions
- Primary: Dynamic permission checklist tailored to user role.
- Edge Case 3.1 (Partial permission grant): Granular fallback state highlighting unassigned scopes with single-click admin escalation trigger.
```