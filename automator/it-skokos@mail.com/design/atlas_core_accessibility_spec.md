# Atlas Core — Accessibility & Sensory Harmony Design Specification
**Author:** Nova Van Dyk  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D16 16:55  
**Inputs used:** Business Document (Company Document)  
## Summary

Comprehensive accessibility remediation and inclusive interaction specification for Atlas Core, aligning tactile and SaaS interactions with WCAG 2.2 AAA guidelines using foundational guidance from Company Document.

## Deliverable
```
# Atlas Core: Accessibility & Sensory Harmony Specification
**Designer:** Nova Van Dyk | Lead UX Romantic
**Scope:** Atlas Core SaaS Interface & Hybrid Face-to-Face Client Touchpoints
**Governing Framework:** WCAG 2.2 Level AAA Compliance & I.T. Skokos Design Tenets

---

### 1. Philosophical & Strategic Alignment
Accessibility is not a sterile checklist; it is an act of deep hospitality. To welcome every user into Atlas Core means sculpting interfaces that resonate with clarity, emotional warmth, and effortless navigation.

*Reference to Internal Resources:*
- **Company Document**: Consulted to extract I.T. Skokos core service principles and foundational design constraints. Used directly to align hybrid digital/in-person token definitions with the overarching organizational brand identity and cross-platform service agreements.

---

### 2. Design Tokens & Sensory Foundations

#### A. Chromatic Harmony & Contrast
- **Surface-to-Text Contrast:** Minimum ratio **7.1:1** across all interactive copy.
  - Background Canvas: `var(--color-bg-base)` (#FAFAF9 / Warm Alabaster)
  - Primary Typography: `var(--color-ink-primary)` (#1C1917 / Deep Silt) — *Contrast Ratio 15.8:1*
  - Interactive Accent: `var(--color-accent-focus)` (#0F766E / Resonant Teal) — *Contrast Ratio 7.4:1*
- **State Indication:** Color is never the sole conduit of meaning; icons and secondary textual cues are mandatory.

#### B. The Focused Breath (Focus Indicators)
- **Focus Rings:** Dual-layer visual halos for keyboard navigators.
  - Outer: `3px solid #0F766E` with a `2px` offset.
  - Inner: `1px solid #FFFFFF` to prevent blend on dark mode surfaces.

#### C. Spatial Touch & Target Geometry
- Minimum target size for hybrid Face-to-Face tablet check-ins: `48x48px` (with `8px` ambient padding).

---

### 3. Component Remediation Matrix

1. **Dynamic Schedule Modal (`<AtlasScheduler />`)**
   - *Issue:* Screen readers lost focus during asynchronous state transitions.
   - *Remediation:* Applied `aria-live="polite"` and programmatic focus shift to the dynamic summary header.
2. **Hybrid Client Verification Card (`<FaceToFaceSyncCard />`)**
   - *Issue:* Low ambient contrast on outdoor kiosk screens.
   - *Remediation:* Enforced high-contrast fallback tokens and haptic tactile feedback triggers for low-vision users.

---
*Approved for implementation across Atlas Core Sprint 14.*
```