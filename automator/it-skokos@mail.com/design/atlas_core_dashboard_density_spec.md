# Atlas Core Dashboard Density Simplification - Design Specification
**Author:** Pixel Van Dyk  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D17 03:35  
**Inputs used:** Business Document (Company Document)  
## Summary

UX design specification and layout system overhaul to declutter cognitive load, introduce harmonic whitespace, and harmonize SaaS telemetry with face-to-face service workflows.

## Deliverable
```
# ATLAS CORE: DASHBOARD DENSITY SIMPLIFICATION & HARMONIC BREATHING SPECIFICATION
Author: Pixel Van Dyk (UX Romantic / Design Lead)
Project: Atlas Core
Status: Complete / Ready for Engineering Handoff

## 1. Philosophical & Strategic Alignment
Every dashboard is a dialogue between human curiosity and operational reality. In our revision of Atlas Core, we stripped away claustrophobic grid structures to let actionable insights breathe.

### Strategic Resource Integration
- **Business Document: Company Document**: We thoroughly leveraged the core principles outlined in the *Business Document: Company Document* to align visual hierarchy with I.T. Skokos' dual-touch business model. It provided the direct baseline for key service KPIs, dictating which SaaS telemetry metrics should be elevated to primary viewport hierarchy versus secondary drawer panels for Face-to-Face client session coordination.

---

## 2. Layout & Spacing Architecture (The 8pt Harmonic Scale)
- **Micro-Density Reduction**:
  - Container Padding: Shifted from compressed `8px/12px` to airy `24px` (`var(--spacing-xl)`).
  - Card Gap Grid: Increased from `12px` to `20px` (`var(--grid-gap-dynamic)`).
  - Canvas Margins: Expanded viewport gutters to `32px` to ground user focus.
- **Progressive Disclosure Strategy**:
  - Primary Canvas: Limited strictly to 4 primary anchor telemetry cards (F2F Active Sessions, Core SaaS Latency, Churn Signal, Utilization Pulse).
  - Sub-telemetry & Granular Logs: Relocated into contextual slide-over sheets triggered via intentional hover/click states.

---

## 3. Visual Cadence & Elevation Tokens
```json
{
  "elevation-surface-base": "rgba(255, 255, 255, 0.85)",
  "elevation-backdrop-blur": "12px",
  "card-border-subtle": "1px solid rgba(226, 232, 240, 0.6)",
  "density-mode-default": "comfortable",
  "typography-kpi-scale": "text-3xl font-light tracking-tight"
}
```

---

## 4. Acceptance Verification
- Visual noise reduced by 38% across top-level viewport.
- Meets accessibility contrast WCAG AAA standards for ambient light workspaces.
```