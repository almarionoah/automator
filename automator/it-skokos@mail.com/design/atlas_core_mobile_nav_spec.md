# Atlas Core: Mobile Navigation Overhaul Design & Interaction Spec
**Author:** Jax Fontaine  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D12 05:15  
**Inputs used:** Business Document (Company Document)  
## Summary

Pragmatic UI/UX specification and component architecture for the Atlas Core mobile navigation overhaul, aligning SaaS tooling and Face-to-Face service flows.

## Deliverable
```
# Atlas Core — Mobile Navigation Overhaul Spec
**Owner:** Jax Fontaine (Design)
**Status:** Ready for Engineering Implementation

## 1. Context & Business Alignment
This overhaul consolidates Atlas Core's navigation for hybrid mobile viewports (<768px). Per the guidance established in the **Company Document**, our information architecture must bridge self-service SaaS capabilities directly with on-demand Face-to-Face service bookings without adding cognitive load.

*Resource Utilization:* 
- **Company Document**: Used to audit tier-one user journeys and ensure core Face-to-Face booking touchpoints sit at root-level priority alongside real-time SaaS platform telemetry.

---

## 2. Navigation Architecture

### A. Bottom App Bar (Fixed Viewport Bottom, 56dp height)
1. **Dashboard** (`/app/dashboard`): Metric cards & quick tenant status.
2. **Services** (`/app/services`): Combined SaaS service catalog + Face-to-Face schedule picker.
3. **Quick Action (FAB)**: Primary modal launch for 'Book Session' or 'New Deployment'.
4. **Activity** (`/app/activity`): Real-time sync logs & appointment notifications.
5. **Account** (`/app/settings`): Workspace switcher, profile, and offline sync toggle.

### B. Drawer / Sheet Interaction (Frictionless Shipper Model)
- **Gesture Target:** Bottom-sheet drawer with drag-to-dismiss threshold (35% velocity trigger).
- **Accessibility:** Minimum touch target 48x48px; contrast ratio >= 4.5:1 (WCAG AA).
- **Micro-transitions:** 200ms ease-out cubic-bezier(0.16, 1, 0.3, 1) for bottom sheet pop.

---

## 3. Token & Asset Variables
```css
:root {
  --nav-bg: #0F172A;
  --nav-active-tint: #38BDF8;
  --nav-inactive-tint: #94A3B8;
  --nav-fab-bg: #2563EB;
  --nav-fab-icon: #FFFFFF;
  --nav-height: 64px;
  --nav-z-index: 1050;
  --nav-border-top: 1px solid rgba(255, 255, 255, 0.08);
}
```

*Handoff complete. Ready for frontend integration in Atlas Core sprint build.*
```