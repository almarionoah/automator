# Design Specification & Token Refactoring: Atlas Core Mobile Navigation Overhaul
**Author:** Sable Reyes  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D16 09:20  
**Inputs used:** Business Document (Company Document)  
## Summary

Refactored mobile navigation architecture, IA tree, and design tokens for Atlas Core, aligning SaaS platform workflows and Face-to-Face service touchpoints with requirements in Business Document: Company Document.

## Deliverable
```
# Design Spec: Atlas Core Mobile Navigation Overhaul (v2.4 Refactor)
**Author:** Sable Reyes (Design Agent) | **Project:** Atlas Core

## 1. Overview & Resource Integration
This overhaul refactors the mobile navigation framework to eliminate legacy layout debt, optimize responsive touch targets, and unify SaaS Platform tooling with Face to Face Services.

- **Resource Reference - Business Document: Company Document**: Utilized as the baseline reference for organizational service taxonomies and brand hierarchy. It directly guided the separation of SaaS tenant management from field-level Face to Face service scheduling workflows, ensuring navigation states accurately reflect compliance and operational tiers.

## 2. Refactored Information Architecture (IA)
- **Primary Bar (Bottom Dock - 56px height, elevation level 3):**
  1. `Dashboard` (`/app/dashboard`) - SaaS core metrics & workspace
  2. `Services` (`/services/f2f`) - Face-to-Face scheduling, client intake, field notes
  3. `QuickAction FAB` (`center-docked`, 48px, token `--action-primary`)
  4. `Analytics` (`/analytics/atlas-core`) - Real-time metrics
  5. `Account` (`/account/tenant`) - Role switcher & settings

## 3. Token Architecture
```css
:root {
  --nav-bg: rgba(18, 20, 24, 0.88);
  --nav-backdrop-blur: 16px;
  --nav-border-subtle: rgba(255, 255, 255, 0.08);
  --nav-item-active: #4F46E5;
  --nav-item-inactive: #94A3B8;
  --nav-touch-target: 48px;
  --nav-spring-easing: cubic-bezier(0.16, 1, 0.3, 1);
  --nav-drawer-z-index: 1200;
}
```

## 4. Interaction & Refactor Improvements
- **Consolidated Component Architecture:** Replaced 8 ad-hoc flyout wrappers with a single polymorphic bottom sheet component (`<AtlasMobileDrawer />`).
- **Touch Target Compliance:** Enforced strict 48x48px interactive bounding boxes across all sub-navigation items.
- **Transitions:** Standardized on a 240ms cubic-bezier spring transition for drawer open/close states.
```