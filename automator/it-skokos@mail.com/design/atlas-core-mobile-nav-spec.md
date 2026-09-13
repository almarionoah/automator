# Atlas Core Mobile Navigation Architecture & Token Spec
**Author:** Jax Okafor  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D17 01:15  
**Inputs used:** Business Document (Company Document)  
## Summary

Complete UI/UX design spec and interaction tokens for the Atlas Core mobile navigation overhaul, unifying SaaS management and Face to Face services.

## Deliverable
```
# Atlas Core — Mobile Navigation Overhaul (v2.0)
**Designer:** Jax Okafor (Design / o3)
**Status:** Ready for Engineering Implementation

## 1. Strategic Context & Resource Reference
This redesign replaces the legacy hamburger menu with an ergonomic bottom-bar and quick-action drawer to streamline hybrid platform access.
- **Business Document: Company Document**: Explicitly referenced to align navigation information architecture with company service hierarchy rules and accessibility standards. Used Section 3 (Service Offerings) to ensure equal visual weighting between core SaaS toolsets and on-demand Face to Face booking workflows.

## 2. Information Architecture
- **Bottom Navigation Bar (Fixed 64px + Safe Area):**
  1. `Dashboard` (`/overview`): Real-time SaaS metric snapshots.
  2. `F2F Services` (`/services/f2f`): Scheduling, client intake, and field agent routing.
  3. `Platform Tools` (`/saas/tools`): Automation runners and workspace controls.
  4. `Activity` (`/notifications`): Unread counts with high-contrast indicator.
  5. `More` (`#sheet-open`): Slide-over sheet for tenant switching and account preferences.

## 3. Touch Targets & Interaction Specs
- **Touch Target:** Minimum 48x48pt active hit box per icon.
- **Transitions:** `transform: translateY` with `cubic-bezier(0.2, 0.0, 0, 1.0)` over 220ms.
- **Drawer Behavior:** Swipe-down-to-dismiss threshold set at 120px velocity offset.
- **Responsive Breakpoint:** Active on viewport widths ≤ 768px; hides when virtual keyboard opens.

## 4. Key Design Tokens
```json
{
  "nav.mobile.bar.height": "64px",
  "nav.mobile.bar.bg": "#0F172A",
  "nav.mobile.item.active": "#38BDF8",
  "nav.mobile.item.inactive": "#94A3B8",
  "nav.mobile.badge.bg": "#EF4444",
  "nav.mobile.sheet.radius": "16px 16px 0 0"
}
```
```