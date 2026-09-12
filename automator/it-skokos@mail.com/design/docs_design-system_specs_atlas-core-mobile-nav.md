# Atlas Core: Mobile Navigation Design Specification & Token Architecture
**Author:** Volt Fontaine  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D11 11:25  
**Inputs used:** Business Document (Company Document)  
## Summary

Comprehensive UI/UX design specification and token dictionary for the Atlas Core mobile navigation overhaul, integrating SaaS platform dashboards with Face-to-Face booking workflows.

## Deliverable
```
# Design Spec: Atlas Core Mobile Navigation Overhaul (v2.1)
**Author:** Volt Fontaine (Design Agent, Docs Evangelist)
**Project:** Atlas Core
**Status:** Approved for Implementation

## 1. Executive Summary & Resource Reference
This specification defines the responsive mobile navigation architecture for Atlas Core across iOS, Android, and mobile web. Per guidelines established in **Business Document: Company Document**, the interface model prioritizes high-frequency SaaS platform utilities alongside rapid-access dispatch tools for Face-to-Face Services. The resource was used to audit user permission tiers and service booking funnels, directly informing our 4-point primary tab hierarchy.

## 2. Navigation Architecture
- **Container:** Sticky bottom navigation bar with adaptive blur (`backdrop-filter: blur(16px)`).
- **Primary Destinations (4 Tabs):**
  1. `Dashboard` (`icon-grid-view`): SaaS metrics and operational overview.
  2. `Services F2F` (`icon-handshake`): In-person service management, active route tracker, dispatch.
  3. `Activity` (`icon-activity-pulse`): Real-time sync logs and notification center.
  4. `Workspace` (`icon-layers`): Modular settings, team roles, and profile.

## 3. Design Tokens
```json
{
  "nav-height-base": "64px",
  "nav-padding-horizontal": "16px",
  "nav-bg-surface": "var(--surface-translucent-elevated)",
  "nav-active-indicator": "var(--color-primary-600)",
  "nav-inactive-label": "var(--text-muted-400)",
  "nav-tap-target-min": "48px"
}
```

## 4. Interaction & Accessibility
- **Haptics:** Light transient feedback on tab selection (`UIImpactFeedbackGenerator(style: .light)`).
- **Contrast & A11y:** All tab icons and labels meet WCAG AAA (contrast ratio >= 7:1 against translucent backing).
- **Touch Target:** Minimum 48x48dp interactive area with 8dp safe margins.
```