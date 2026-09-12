# Atlas Core Lean Onboarding Flow Specification
**Author:** Iris Fontaine  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D13 19:45  
**Inputs used:** Business Document (Company Document)  
## Summary

A cost-optimized, zero-dependency 3-step onboarding flow design spec for Atlas Core, eliminating third-party tour SaaS licensing and heavy CDN assets in alignment with the Company Document.

## Deliverable
```
# ATLAS CORE — ONBOARDING FLOW REDESIGN SPECIFICATION
**Designer:** Iris Fontaine | **Project:** Atlas Core | **Discipline:** Lean Product Design

## 1. Strategic Objectives & Cost Optimization
In alignment with the operational cost-reduction targets defined in the **Company Document**, this rework replaces our previous asset-heavy onboarding sequence and eliminates the external third-party product tour subscription. By transitioning to a native, lightweight modal system, we remove 4.8MB of video/lottie assets from CDN distribution and lower client-side runtime memory usage.

## 2. Reworked 3-Step Flow Architecture

### Step 1: Workspace Initialization (Context Selection)
- **UI:** Compact modal (480px width) utilizing existing system components.
- **Input:** Workspace Name & Operational Mode (`SaaS Platform` vs `Hybrid Face-to-Face Services`), referencing tier structures from the **Company Document**.
- **Optimization:** Zero illustration assets; uses clean semantic typography and native CSS borders.

### Step 2: Role & Telemetry Baseline
- **UI:** Single-select role picker (Administrator, Practitioner, Viewer).
- **Mechanism:** Automatically provisions default dashboard layout based on selected role, bypassing the need for an interactive tutorial overlay.
- **Asset Budget:** 0 HTTP requests (inline SVG icons from shared design tokens).

### Step 3: Fast-Track Activation
- **UI:** Confirmation summary with primary CTA: `Launch Atlas Core`.
- **Action:** Triggers background sync and directs immediately to the populated workspace. Eliminates multi-slide walkthroughs that previously caused a 28% drop-off.

## 3. UI Token & Performance Budgets
- **Component Overhead:** Native `ds-modal`, `ds-button`, `ds-radio-group`.
- **Typography:** System font stack (`-apple-system, BlinkMacSystemFont, Segoe UI, Roboto`) to avoid custom webfont payload.
- **Bundle Footprint:** < 4KB total JS/CSS (previously 162KB with third-party tour vendor).
- **Target Completion Rate:** >= 91% completion within 45 seconds.
```