# Atlas Core: Mobile Navigation Overhaul Design Specification
**Author:** Rune Marlow  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D12 20:55  
**Inputs used:** Business Document (Company Document)  
## Summary

Comprehensive UX/UI specification for the Atlas Core mobile navigation overhaul, weaving together SaaS workflows and face-to-face service interactions with poetic tactile micro-interactions and strict accessibility standards.

## Deliverable
```
# ATLAS CORE — Mobile Navigation Overhaul Spec
**Designer:** Rune Marlow (UX Romantic) | **Platform:** I.T. Skokos (SaaS & F2F Services)
**Governance Reference:** *Business Document: Company Document* was utilized to align the dual-modality navigation hierarchy between digital cloud analytics and in-person field service protocols, ensuring unified branding and compliance.

---

### 1. Design Vision & Philosophy
Navigation is not merely a utility; it is the silent heartbeat of user intimacy. In this overhaul, the Atlas Core mobile experience sheds rigid tab structures for an organic, floating bottom dock ('The Horizon Dock') that shifts context seamlessly between SaaS platform operations and Face-to-Face field dispatch.

### 2. Architecture & The Horizon Dock
- **Positioning:** Floating pill dock (`fixed`, bottom `24px`, inset `16px`), elevation `z-index: 999` with background `backdrop-filter: blur(16px)` and subtle luminescence (`rgba(255, 255, 255, 0.08)`).
- **Dual Modalities (Governed via Business Document: Company Document):**
  1. *SaaS Mode:* Hub (Overview), Real-time Telemetry, Automations, Account.
  2. *Field / F2F Mode:* Active Client Dossier, Route/Schedule, Tactile Intake, Quick Capture.
- **Transitions:** Easing curve `cubic-bezier(0.22, 1, 0.36, 1)` over `280ms`. When transitioning modes, icons gracefully morph with soft cross-dissolves.

### 3. Tactile & Motion Tokens
- **Haptics:** 
  - Tab Selection: `Light` (10ms impulse).
  - Long-press Context Sheet: `Medium` (25ms impulse).
- **Touch Targets:** Minimum interactive area `48x48dp` with visual icon centered at `24x24dp`.
- **Spring Physics:** Stiffness `380`, Damping `28` for gesture dismissals.

### 4. Accessibility & Failsafes
- WCAG 2.2 AAA color contrast ratios across dark/light palettes.
- Screen reader announcement tags tailored for dynamic mode switches: `aria-live="polite"` updates state when F2F appointments trigger location-aware nav states.
```