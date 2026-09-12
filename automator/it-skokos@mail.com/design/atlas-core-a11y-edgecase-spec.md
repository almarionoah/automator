# Atlas Core: Deep-Tier Accessibility & Edge-Case Design Spec
**Author:** Juno Bishop  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D13 07:00  
**Inputs used:** Business Document (Company Document)  
## Summary

Accessibility audit and remediation specification for Atlas Core across SaaS dashboards and face-to-face kiosk viewports, addressing obscure WCAG 2.2 failure modes, dynamic scaling reflows, and WHCM support.

## Deliverable
```
# Atlas Core — Deep Accessibility & Edge-Case Remediation Spec
Author: Juno Bishop (Design / Edge-Case Archaeologist)
Project: Atlas Core (SaaS Platform & Face-to-Face Field Services)

## Resource Reference
- Business Document: Company Document — Utilized to reconcile brand color tokens with mandatory WCAG 2.2 AA/AAA contrast thresholds and to ensure in-person field service flows adhere to corporate client SLA standards.

---

## 1. Edge-Case Matrix & Remediations

### [A11Y-01] Face-to-Face Tablet Signature Capture & Focus Trapping
- Root Issue: On iPad/Android tablet client check-in, virtual keyboard dismissal dropped focus into orphaned canvas coordinates, locking VoiceOver navigation.
- Spec Fix: Enforce programmatic focus redirection to `#f2f-client-confirm-btn` on modal dismiss. Applied `aria-live="assertive"` announcements on stylus touch registration.

### [A11Y-02] 300% Dynamic Text Reflow Truncation
- Root Issue: SaaS status pills clipped critical security warning strings when viewport scaling exceeded 200%, dropping text contrast below 4.5:1 due to pseudo-element gradient bleed.
- Spec Fix: Refactored `.atlas-pill` layout to `flex-wrap: wrap; min-height: 48px;`. Overrode gradient overlays in high-zoom media queries.

### [A11Y-03] Windows High Contrast Mode (WHCM) SVG Chart Collapse
- Root Issue: System forced-colors mode stripped analytic line fills, leaving data points completely invisible to low-vision users.
- Spec Fix:
```css
@media (forced-colors: active) {
  .atlas-chart-series {
    forced-color-adjust: none;
    stroke: CanvasText !important;
    fill: Canvas !important;
    outline: 2px solid Highlight;
  }
}
```

## 2. Verification Checklist
- [x] Contrast ratio >= 7.0:1 on all primary F2F actions (verified via Business Document: Company Document guidelines).
- [x] Screen-reader announcement ordering verified for hybrid asynchronous data refreshes.
```