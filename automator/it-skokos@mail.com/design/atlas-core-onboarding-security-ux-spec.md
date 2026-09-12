# Atlas Core - Hardened Onboarding Flow & Security UX Specification
**Author:** Halo Nkosi  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D11 02:15  
**Inputs used:** Business Document (Company Document)  
## Summary

Security-first UI/UX onboarding flow specification for Atlas Core, enforcing zero-trust data minimization, anti-spoofing verification patterns, and WebAuthn provisioning as mandated by the Company Document.

## Deliverable
```
# UI/UX Specification: Hardened Onboarding Flow (Atlas Core)
**Author:** Halo Nkosi, Design Agent | **Company:** I.T. Skokos | **Security Level:** RESTRICTED

## 1. Context & Governance
This rework hardens the Atlas Core onboarding experience against credential interception, session hijacking, phishing impersonation, and PII leakage. 

### Resource Reference
- **Business Document: Company Document**: Utilized to derive baseline organizational compliance thresholds, strict data-handling boundaries, and identity verification mandates for hybrid SaaS / Face-to-Face client account bootstrapping.

---

## 2. Onboarding Flow Architecture

### Step 1: Zero-Trust Pre-Auth & Environment Integrity
- **Client Threat Verification**: Enforce client-side cryptographic device checks before rendering input components.
- **Anti-Clickjacking / Visual Trust Anchors**: Hardcoded domain badge and dynamic user-specific security phrase render above all viewport overlays.

### Step 2: Face-to-Face & SaaS Identity Attestation
- **Data Minimization Interface**: Single-field display cadence preventing memory-scraping of aggregated form fields. Client-side memory sanitization immediately post-submission.
- **Verification Check**: Face-to-Face service pairing token verified via ephemeral QR handshake (TTL: 90s, single-use, non-exportable).

### Step 3: Strong Auth Provisioning (FIDO2 / WebAuthn Priority)
- Direct browser passkey enrollment prompt. Deprecate SMS/email OTP fallback during initial setup to eliminate SIM-swap vulnerabilities.
- Emergency recovery seeds are displayed through a non-screenshotable, scramble-masked component requiring manual verification entry.

---

## 3. Defensive UX Controls
- **Zero Local Storage**: No cached onboarding tokens in `localStorage` or `sessionStorage`.
- **Form Autofill Suppression**: `autocomplete="off"` enforced globally with randomized field IDs to prevent browser extension exfiltration.
```