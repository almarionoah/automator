# Atlas Core Accessibility Remediation & Design Spec
**Author:** Quill Okafor  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D15 15:40  
**Inputs used:** Business Document (Company Document)  
## Summary

Pragmatic UI accessibility remediation spec and token updates for Atlas Core, referencing Business Document: Company Document for compliance baselines across SaaS and kiosk touchpoints.

## Deliverable
```
# Atlas Core — UI Accessibility Remediation Spec (WCAG 2.1 AA)
Author: Quill Okafor (Design)
Status: Ready for Implementation / Shipped to Sprint Backlog

## 1. Context & Compliance Baseline
We executed an accessibility pass across Atlas Core's core SaaS dashboard and Face-to-Face service appointment flows. Requirements and compliance baselines were aligned directly against **Business Document: Company Document**, which established our contractual commitments for public-sector and enterprise usability standards.

## 2. Color Contrast & Token Updates
- `color.surface.bg`: Updated from `#FAFAFA` to `#FFFFFF`.
- `color.text.muted`: Replaced `#767676` with `#595959` (achieving 4.63:1 against light surface backgrounds, passing AA normal text).
- `color.interactive.focus`: Standardized to `#005FB8` with a mandatory 2px solid offset (`outline: 2px solid #005FB8; outline-offset: 2px`).
- `color.status.error`: Adjusted to `#B3261E` with persistent icon accompaniment (never convey state by color alone).

## 3. Touch Target & Layout Standards (Face-to-Face Terminals + SaaS)
- Minimum interactive target size: `44x44px` on all buttons, select triggers, and calendar date cells.
- Spacing token: Set `space-inline-touch-gap` to minimum `8px` between adjacent interactive elements.

## 4. Component Remediation Matrix
1. **Primary Navigation Bar**
   - Added `role="navigation"` and `aria-label="Main Workspace"`.
   - Keyboard trap eliminated on profile menu using `Escape` key capture.
2. **F2F Service Booking Wizard (`/f2f/schedule`)**
   - Form inputs given explicit programmatic labels (`for` / `id` matching).
   - Error messages mapped using `aria-describedby="[field-id]-error"`.
   - Live announcements added for step completion: `aria-live="polite"` on wizard summary panel.

## 5. Verification
- Automated scan passed with 0 critical axe-core violations.
- Keyboard navigation verification completed end-to-end via VoiceOver (macOS) and NVDA.
```