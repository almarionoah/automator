# Atlas Core - Mobile Navigation Overhaul Design Spec & Token Mapping
**Author:** Jax Okafor  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D17 01:40  
**Inputs used:** Business Document (Company Document)  
## Summary

Pragmatic mobile navigation design specification and component breakdown for Atlas Core, integrating SaaS tools and Face to Face booking workflows per Business Document: Company Document.

## Deliverable
```
# Design Spec: Atlas Core Mobile Navigation Overhaul
**Owner:** Jax Okafor (Design)
**Project:** Atlas Core | **Status:** Ready for Engineering

## 1. Context & Governance
Aligned with guidelines established in **Business Document: Company Document**, which outlines our unified brand hierarchy across SaaS telemetry and Face to Face field service operations. We utilized **Business Document: Company Document** specifically to determine route priority, IA grouping (separating real-time platform metrics from field dispatch scheduling), and minimum compliance targets for touch accessibility.

## 2. Navigation Architecture
- **Primary Navigation (Sticky Bottom Bar):** 4 key anchors + 1 contextual action trigger.
  - `[0]` Dashboard (SaaS Platform Overview)
  - `[1]` F2F Services (Field scheduling & in-person queue)
  - `[2]` Quick Action (`+` Sheet: New Session / New Ticket)
  - `[3]` Telemetry (Real-time logs)
  - `[4]` Account / Workspace Switcher
- **Secondary Drawer (Hamburger Trigger):** Global settings, billing tiers, API keys, compliance logs.

## 3. Interaction & Gestures
- **Touch Targets:** Minimum 48x48dp interactive bounding boxes.
- **Quick Action Sheet:** Velocity-tracked swipe down (`threshold: 120px`, `spring: { damping: 24, stiffness: 280 }`).
- **Haptics:** Light haptic feedback on tab change and sheet snap points.

## 4. Token & Styling Contract
```css
:root {
  --nav-bg: rgba(18, 20, 24, 0.88);
  --nav-backdrop-blur: 16px;
  --nav-border: rgba(255, 255, 255, 0.08);
  --nav-item-active: #3B82F6;
  --nav-item-inactive: #94A3B8;
  --nav-sheet-radius: 20px 20px 0 0;
  --nav-safe-area-bottom: env(safe-area-inset-bottom, 16px);
}
```

## 5. Handoff Checklist
- [x] Figma components linked to Atlas Core Design Library.
- [x] Tested on iOS (WebKit safe-areas) and Android (gesture bar overlap).
- [x] Fallback layout verified for small viewports (360px).
```