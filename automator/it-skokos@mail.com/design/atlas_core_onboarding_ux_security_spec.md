# Atlas Core - Secure Onboarding Flow Redesign Specification
**Author:** Nyx Ito  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D12 18:10  
**Inputs used:** Business Document (Company Document)  
## Summary

Comprehensive UX/UI security and interaction design specification for Atlas Core's reworked onboarding flow, enforcing zero-trust data entry, strict session segregation, and hybrid SaaS-to-Face-to-Face verification safeguards.

## Deliverable
```
# Design Specification: Atlas Core Secure Onboarding Flow (v2.4)
**Author:** Nyx Ito, Product Design
**Status:** Approved for Implementation (Security Hardened)

## 1. Context & Governance Reference
This redesign references and implements the baseline compliance and tenant provisioning constraints mandated in **Business Document: Company Document**. Specifically, the resource was used to audit data minimization requirements, ensuring that identity collection at registration strictly prevents over-retention of client PII during hybrid SaaS and Face to Face handoffs.

## 2. Onboarding Flow Architecture & Threat Surface Controls

### Step 1: Zero-Exposure Tenant Initialization
- **Input Sanitization Cues:** Real-time visual entropy indicators on client-side secret inputs; masking active by default.
- **Link Security:** Discarded magic-link fallback. Onboarding relies strictly on ephemeral cryptographic invite tokens with a strict 15-minute TTL. No session state persisted in `localStorage`.

### Step 2: Adaptive Multi-Factor Enrollment (FIDO2 / WebAuthn Priority)
- **Interaction Pattern:** Immediate WebAuthn hardware key / biometric enrollment prompt before any profile metadata entry.
- **Fallback UI:** Enforces strict TOTP setup with obscured backup codes rendered behind explicit user-initiated unmasking actions.

### Step 3: Hybrid Service Verification Protocol (Face-to-Face Bridge)
- **Mechanism:** For clients utilizing I.T. Skokos Face to Face Services, the SaaS onboarding generates a dynamic, single-use, time-bound QR code (AES-256 wrapped nonce).
- **Security Invariant:** In-person field agents must verify the dynamic cryptographic token alongside physical identity proof prior to tenant unlocking.

### Step 4: Least-Privilege Role Provisioning UI
- **Permission Matrix UX:** Explicit opt-in permission toggles default to lowest-privilege scope. Visual warnings trigger on high-privilege permission assignment.
```