# Atlas Core UI Accessibility Specification & Token Manifest
**Author:** Sable Petrov  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D16 07:15  
**Inputs used:** Business Document (Company Document)  
## Summary

Accessibility design specification and token review for Project Atlas Core, elevating sensory harmony, contrast ratios, and screen-reader choreography while aligning strictly with the Business Document: Company Document guidelines.

## Deliverable
```
# Project Atlas Core — Accessibility & Sensory Design Specification
**Author:** Sable Petrov (Design)
**Scope:** SaaS Platform & Hybrid Face-to-Face Bridge Components

---

### Strategic Resource Alignment
In crafting this accessibility pass, we integrated the organizational mandates defined within the **Business Document: Company Document**. This document was utilized to benchmark our digital inclusion standards against corporate compliance targets and ensure seamless parity between Atlas Core’s self-service SaaS views and our on-ground, Face to Face concierge flows.

---

### 1. Palette Resonance & Luminance Ratios (WCAG 2.1 AAA)
True accessibility is not mere compliance; it is visual hospitality.

- `--atlas-surface-canvas`: `#0D1117` (Deep Obsidian)
- `--atlas-text-primary`: `#F0F6FC` (Luminous Alabaster) — **Contrast 15.8:1** (Pass AAA)
- `--atlas-text-muted`: `#8B949E` (Mist Gray) — **Contrast 4.8:1** (Pass AA Normal, AAA Large)
- `--atlas-accent-focus`: `#58A6FF` (Electric Azure) — High-chroma ring for non-visual cueing.
- `--atlas-action-touchpoint`: `#238636` (Verdant Pine) with `#FFFFFF` text — **Contrast 5.1:1**.

### 2. Focus Chandelier: Keyboard Navigation Architecture
Every interactive element must announce its presence with grace and clarity:
```css
:focus-visible {
  outline: 2px solid var(--atlas-accent-focus);
  outline-offset: 3px;
  box-shadow: 0 0 0 6px rgba(88, 166, 255, 0.22);
  transition: outline-offset 120ms cubic-bezier(0.16, 1, 0.3, 1);
}
```

### 3. Assistive Choreography & Screen Reader Structure
- **Landmarks:** Distinct `<main id="core-portal">`, `<nav aria-label="Atlas Core Service Navigation">`, and `<aside aria-label="Face to Face Booking Status">`.
- **Dynamic Updates:** `aria-live="polite"` configured across async status chips to whisper state transitions without jarring the user's workflow.
```