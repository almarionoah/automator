# Atlas Core - Secure Onboarding Flow Design Specification (v2.4)
**Author:** Lyra Okafor  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D19 11:35  
**Inputs used:** Business Document (Company Document)  
## Summary

Complete redesign specification of the Atlas Core onboarding journey, implementing strict data minimization, step-up MFA, zero PII caching, and privacy-first UI patterns aligned with internal compliance standards.

## Deliverable
```
# Design Specification: Atlas Core Secure Onboarding Flow
**Author:** Lyra Okafor (Design)
**Project:** Atlas Core | I.T. Skokos
**Classification:** Internal Restricted

## 1. Context & Governance Reference
This redesign restructures the initial user intake for Atlas Core to eliminate credential sniffing vectors and client-side PII leakage. During specification, the **Business Document: Company Document** was used to determine the mandatory data collection thresholds, legal identity verification requirements for Face-to-Face service components, and strict data retention constraints governing SaaS tenancy initialization.

## 2. Onboarding Flow Architecture

### Step 1: Zero-Leak Identity Registration
- **UI Layout:** Minimalist single-field focus. Disables browser autofill/autocomplete (`autocomplete="off"`, `autocorrect="off"`).
- **Security Controls:** Password input field masks characters after 250ms. Real-time zxcvbn entropy meter rendered client-side without sending keystroke telemetry to backend.
- **Face-to-Face Hybrid Verification:** If physical verification is selected per **Business Document: Company Document**, prompt presents one-time ephemeral QR badge with 90s TTL.

### Step 2: Mandatory Step-Up Authentication Setup
- **MFA Enrolment Screen:** WebAuthn/FIDO2 hardware key primary recommendation; TOTP secondary. SMS authentication explicitly excluded.
- **Recovery Key Generation:** 24-word seed visual confirmation. Requires forced manual selection verification to confirm key storage before enabling "Continue" button.

### Step 3: Workspace & Role Scoping
- **Role-Based Permission Matrix:** Explicit checkbox consents. Pre-checked boxes are strictly prohibited.
- **Session Integrity:** 180-second inactivity lock screen with secure session teardown.

## 3. Design System Tokens & Hardening Rules
- Input sanitization feedback rendered via isolated SVG icons (no arbitrary HTML injection).
- High-contrast visual alerts for sensitive access requests.
- All previews display masked metadata (e.g., `usr_****3a9`) until authenticated unlock.
```