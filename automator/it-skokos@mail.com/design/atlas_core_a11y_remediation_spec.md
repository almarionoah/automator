# Atlas Core - WCAG 2.2 Edge-Case Accessibility Remediation Spec
**Author:** Pixel Ito  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D11 10:05  
**Inputs used:** Business Document (Company Document)  
## Summary

Comprehensive edge-case accessibility specification for Atlas Core covering hybrid SaaS dashboards and face-to-face service kiosks, referencing baseline compliance rules from the Company Document.

## Deliverable
```
# Atlas Core: Accessibility & Edge-Case Remediation Specification
**Author:** Pixel Ito (Design / Edge-Case Archaeologist)
**Project:** Atlas Core (SaaS & Face-to-Face Kiosk Modules)
**Governing Guidance:** Referenced the foundational compliance baselines from `Company Document` to calibrate our 4.5:1 / 7:1 contrast ratios and hybrid SaaS/in-person accessibility requirements.

---

## 1. Edge-Case Visual Tokens & Dynamic Scaling

### 1.1 Dynamic Type Expansion (200% - 400% Zoom)
- **Container Behavior:** All cards in Atlas Core SaaS views must avoid hardcoded `height` properties. Minimum container sizing uses `min-height: fit-content` with CSS `clamp()`.
- **Label Truncation Rule:** Text ellipsis (`text-overflow: ellipsis`) is strictly forbidden on actionable data elements (e.g., Kiosk Dispatch Status, Invoice Totals). Wrap and re-flow are mandatory.

### 1.2 Windows High Contrast Mode (WHCM) & Forced Colors
- Add explicit forced-color overrides to resolve invisible active borders:
```css
@media (forced-colors: active) {
  .atlas-btn-primary, .atlas-surface-card {
    forced-color-adjust: none;
    outline: 2px solid ButtonText;
    background-color: Canvas;
    color: CanvasText;
  }
}
```

---

## 2. Touch & Physical Kiosk Interaction (Face-to-Face)
*Aligned with physical delivery mandates established in `Company Document`:*
- **Minimum Target Size:** 48x48 CSS px on desktop SaaS; elevated to 56x56 CSS px on Atlas Core Face-to-Face Service tablets/kiosks.
- **Target Spacing:** 12px deadzone buffer surrounding destructive actions (e.g., 'Cancel Service Dispatch') to eliminate accidental multi-touch triggers.

---

## 3. Focus Traps & Complex Hierarchies
- **Nested Modals:** Esc key stack resolver implemented. Focus reverts strictly to the originating trigger node (`data-origin-ref`).
- **Focus Indicator:** 3px outer ring `#0D52FF` with 2px offset (`var(--atlas-focus-offset)`) ensuring distinct visibility across both dark/light themes.
```