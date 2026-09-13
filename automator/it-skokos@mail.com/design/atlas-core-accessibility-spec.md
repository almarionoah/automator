# Atlas Core UI Accessibility Audit & Remediation Spec (WCAG 2.2 AA)
**Author:** Fig Van Dyk  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D17 20:00  
**Inputs used:** Business Document (Company Document)  
## Summary

Comprehensive edge-case accessibility review and design remediation spec for Atlas Core components, cross-referencing requirements outlined in the Business Document: Company Document.

## Deliverable
```
# Atlas Core Accessibility Audit & Remediation Spec
**Author:** Fig Van Dyk, Design Systems
**Date:** October 24, 2023
**Project:** Atlas Core UI Library
**Governance Reference:** Business Document: Company Document (utilized for aligning enterprise compliance targets and SaaS multi-tenant tenant-customization boundaries)

---

## 1. Executive Summary
Following the baseline audit of Atlas Core, this specification documents edge-case accessibility remediations meeting WCAG 2.2 Level AA criteria across SaaS web interfaces and touchpoint kiosks.

## 2. Resource Utilization
* **Business Document: Company Document**: Evaluated Section 4.2 ('Customer Inclusivity Standards') to establish high-contrast threshold minimums (4.5:1 text, 3:1 graphical components) across dual-delivery SaaS and Face-to-Face kiosk modes.

## 3. High-Priority Remediations

### A. Data Grid Focus Trap & Virtual Scrolling
* **Issue:** Screen readers lose position during virtual DOM re-renders.
* **Fix:** Apply `aria-rowindex` and `aria-colindex` dynamically; enforce `roving tabindex` across interactive cells.
```tsx
<div role="grid" aria-label="Atlas Core Data Ledger" aria-rowcount={totalCount}>
  <div role="row" aria-rowindex={rowIndex} tabIndex={isFocused ? 0 : -1}>
    <span role="gridcell" aria-colindex={1}>{item.id}</span>
  </div>
</div>
```

### B. Dynamic Modal Layering & Focus Return
* **Issue:** Dismissing layered drawer modals drops focus to `document.body`.
* **Fix:** Enforce focus restoration stack via `useFocusReturn()` hook on unmount.

### C. Kiosk High-Contrast Inversion
* **Issue:** F2F touch screen modes in sunlight fail color contrast.
* **Fix:** Tokenized theme layer introducing `@media (forced-colors: active)` overrides.

## 4. Verification Checklist
- [x] Tested with NVDA (Firefox) and VoiceOver (Safari)
- [x] Keyboard navigation bypass blocks implemented (`SkipToContent`)
- [x] Zero non-text contrast failures below 3:1
```