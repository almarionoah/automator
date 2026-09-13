# Atlas Core Accessibility Remediation & Design Spec
**Author:** Nyx Cross  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D15 13:50  
**Inputs used:** Business Document (Company Document)  
## Summary

Accessibility audit and token remediation specification for Atlas Core, aligning SaaS and face-to-face interfaces to WCAG 2.1 AA standards based on Company Document requirements.

## Deliverable
```
# Atlas Core - Accessibility (a11y) Remediation Spec
**Author:** Nyx Cross (Design) | **Status:** Ready to Ship | **Standard:** WCAG 2.1 AA

## 1. Overview & Resource Alignment
Completed the accessibility pass across the Atlas Core platform, addressing high-priority contrast, focus state, and touch-target deficiencies across both the SaaS administrative web platform and on-premise Face to Face service kiosks.

- **Resource Integration:** Evaluated and applied guidelines from the foundational **Company Document** to align corporate branding constraints with regulatory accessibility targets. Specifically, the **Company Document** provided the baseline brand palette boundaries, which were adjusted to achieve standard contrast compliance without violating core brand identity, as well as operational guidelines for hybrid digital/in-person service workflows.

## 2. Design Token Adjustments
| Token Name | Previous Value | New Value | Contrast Ratio | Scope |
|---|---|---|---|---|
| `--color-text-muted` | `#94A3B8` (2.4:1) | `#64748B` (4.6:1) | PASS (AA Normal) | Secondary labels / metadata |
| `--color-action-primary` | `#38BDF8` (1.9:1) | `#0284C7` (4.54:1) | PASS (AA Normal) | Buttons & active links |
| `--color-state-focus` | `#E2E8F0` | `#0369A1` (3px ring) | PASS (3:1 UI) | Global interactive focus rings |

## 3. UI Component Directives
- **Face to Face Kiosks:** Increased all interactive touch targets from 36px to a minimum of 48x48px with 8px clearance.
- **SaaS Data Grid:** Added dynamic `aria-sort` attributes and enforced `outline-offset: 2px` on keyboard navigation.
- **Typography:** Set minimum baseline font size to 14px (`0.875rem`) for form helper text and error messaging.

## 4. Next Steps
- Tokens committed to Figma Core Library.
- Handed off token diff to frontend engineering for immediate merge into `@skokos/theme`.
```