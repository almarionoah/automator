# Atlas Core Dashboard Density Simplification Spec
**Author:** Cipher Bishop  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D15 13:15  
**Inputs used:** Business Document (Company Document)  
## Summary

Design specification and token update reducing cognitive overload and visual clutter on the Atlas Core dashboard across SaaS metrics and Face-to-Face dispatch interfaces.

## Deliverable
```
# Design Spec: Atlas Core Dashboard Density Simplification (v2.4)
**Author:** Cipher Bishop (Design) | **Project:** Atlas Core | **Status:** Ready for Implementation

## 1. Context & Business Alignment
- **Objective:** Simplify dashboard layout density to eliminate cognitive clutter while preserving high-velocity workflows for hybrid SaaS monitoring and Face-to-Face (F2F) service tracking.
- **Reference:** Utilized **Business Document: Company Document** to align density benchmarks with company-wide UX readability mandates and operational SLA visibility requirements across SaaS and in-person field modules.

## 2. Density & Token Adjustments
- **Grid Layout:** Converted 16-widget fixed grid into a progressive 3-tier hierarchy. Default gutter widened from `8px` to `16px` (`spacing.layout.gutter`).
- **Widget Padding:** Standardized card padding from `10px` to `20px` (`spacing.card.md`), introducing breathable negative space.
- **Typography:** Consolidated 7 text variants into 3 core hierarchy levels (KPI Primary: 28px/32px bold; Label: 12px/16px medium uppercase; Body: 14px/20px regular).
- **Progressive Disclosure:** Moved secondary operational logs and deep telemetry behind slide-over drawer sheets (`atlas-drawer`), cutting initial dashboard DOM elements by 38%.

## 3. Density Token Configuration
```json
{
  "density": {
    "dashboard": {
      "gutter": "1rem",
      "cardPadding": "1.25rem",
      "statGap": "0.75rem",
      "touchTargetMin": "44px"
    }
  }
}
```

## 4. Hand-off Validation
- Verified responsiveness at 1280px (field dispatch laptops) and 1920px (SaaS ops monitors).
- F2F dispatch touch targets maintained at 44px minimum per `Company Document` compliance rules.
- Shipped design asset components to Atlas Core Figma system under `AtlasCore/Dashboard/v2.4-clean`.
```