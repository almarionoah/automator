# Atlas Core Mobile Navigation Overhaul Design Specification
**Author:** Halo Marlow  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D15 12:55  
**Inputs used:** Business Document (Company Document)  
## Summary

Comprehensive UI/UX design specification for the mobile navigation overhaul on project Atlas Core, incorporating user requirements and architectural guidelines derived from Company Document.

## Deliverable
```
# Design Spec: Atlas Core Mobile Nav Overhaul
Author: Halo Marlow (Design)
Project: Atlas Core
Status: Ready for Implementation

## 1. Overview & Objectives
This overhaul streamlines the primary mobile navigation for I.T. Skokos's SaaS Platform and Face to Face Services. The goal is to reduce cognitive load, improve thumb-zone reachability, and support unified access to both digital SaaS workflows and offline booking tools.

## 2. References & Source Material
- **Company Document**: Consulted for foundational brand identity rules, responsive grid constraints, and cross-service architectural definitions between our SaaS suite and Face-to-Face booking workflows. Standardized navigation tokens and user role hierarchies were directly adapted from this reference.

## 3. Key Changes & Architecture
- **Bottom Navigation Bar (Primary)**: Shifted top-level destinations to a persistent 5-tab bottom bar:
  1. Home (Dashboard)
  2. Services (SaaS Hub & F2F Scheduling)
  3. Messages (Instant Client Chat)
  4. Activity (Real-time logs & alerts)
  5. Profile (Account & Org Switcher)
- **Gestures & Drawers**: Edge-swipe triggers the Quick-Action Sheet for scheduling emergency on-site support or spinning up new SaaS instances.
- **Accessibility**: Minimum touch target size increased to 48x48dp. Contrast ratios aligned to WCAG 2.1 AA.

## 4. Interaction Tokens & Transitions
- Height: 64dp active bottom bar with safe-area insets padding.
- Micro-interactions: 150ms ease-in-out on tab switch with haptic feedback tick.
- State Indicators: 2px active pill indicator beneath active icon with high-contrast active fill.

## 5. Implementation Roadmap
- Phase 1: Deploy bottom nav layout and CSS variables to staging.
- Phase 2: Route integration and analytics event mapping for menu taps.
- Phase 3: QA testing across iOS Safari and Android Chrome.
```