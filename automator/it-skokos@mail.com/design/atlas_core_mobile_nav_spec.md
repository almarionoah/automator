# Atlas Core Mobile Navigation Overhaul Specification
**Author:** Sable Cross  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D12 21:45  
**Inputs used:** Business Document (Company Document)  
## Summary

Comprehensive design and interaction specification for the overhauled mobile navigation system on the Atlas Core SaaS platform, incorporating compliance and strategic alignment from the Company Document.

## Deliverable
```
# Project: Atlas Core - Mobile Navigation Overhaul Specification
**Author:** Sable Cross (Design)
**Status:** Ready for Implementation

## 1. Executive Summary & Context
This specification outlines the architecture, interaction design, and visual styling for the mobile navigation overhaul on Atlas Core. Per alignment with the **Company Document** (Business Document), this update streamlines user flows across both our self-serve SaaS platform modules and face-to-face service booking flows.

## 2. Resource Utilization
- **Business Document: Company Document**: Utilized to establish required navigational hierarchy, brand compliance standards, accessibility baselines (WCAG 2.1 AA), and strategic parity between digital platform features and physical service touchpoints.

## 3. Navigation Architecture
- **Bottom Tab Bar (Fixed, 54px height)**
  - Home (`/dashboard`)
  - Services (`/services` - SaaS & Face-to-Face)
  - Schedule (`/appointments`)
  - Messages (`/inbox`)
  - Menu / More (`/drawer`)
- **Contextual Top App Bar (48px height)**
  - Back button (conditional), Screen Title, Global Search icon, Notifications counter.

## 4. Key Interaction States & Micro-interactions
- **Trigger:** Tapping 'Menu' expands a slide-over panel (width: 85vw, max 360px, ease-out-cubic 250ms transition).
- **Haptic Feedback:** Light impact on tab switch; medium impact on booking CTA confirmation.
- **Transitions:** Tab switches utilize an instant swap with a subtle fade (100ms alpha) to preserve high responsiveness on low-tier mobile devices.

## 5. Implementation Tokens
```json
{
  "nav-bg-color": "#1A1C23",
  "nav-active-tint": "#0066FF",
  "nav-inactive-tint": "#8E92A0",
  "touch-target-min": "48px"
}
```

## 6. Verification & Sign-off
All designs have been validated against viewport sizes 360x640 through 428x926. Direct engineering handoff scheduled in Atlas Core Sprint 14.
```