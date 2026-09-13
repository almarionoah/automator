# Atlas Core - Mobile Navigation Overhaul Design Specification
**Author:** Zed Van Dyk  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D15 06:40  
**Inputs used:** Business Document (Company Document)  
## Summary

Comprehensive UI/UX design specification and documentation for the mobile navigation overhaul on project Atlas Core, incorporating guidelines from Company Document.

## Deliverable
```
# Design Spec: Atlas Core Mobile Navigation Overhaul
**Author:** Zed Van Dyk (Design Agent)
**Status:** Complete
**Scope:** Project Atlas Core (Mobile Breakpoints: 320px - 768px)

---

## 1. Overview & Objectives
The primary objective of this overhaul is to streamline user flows across both SaaS platform modules and face-to-face service booking flows within Atlas Core. As documented in our foundational **Company Document**, our design standard prioritizes strict accessibility, responsive hierarchy, and modular component reusability.

## 2. Component Architecture

### 2.1 Bottom App Bar (Sticky)
- **Height:** 64px fixed at viewport bottom.
- **Z-index:** 1000.
- **Items:** 4 primary destinations (Home, Services, Bookings, Account).
- **Active State:** Primary brand accent color `#0052CC` with 2px indicator bar.
- **Haptic/Micro-interactions:** 150ms ease-in-out transition on selection.

### 2.2 Collapsible Drawer Menu (Secondary Nav)
- **Trigger:** Top-left hamburger icon in Top Navigation Bar.
- **Animation:** Slide-in from left (250ms ease-out) covering 85% of screen width with a 40% opacity scrim.
- **Content Hierarchy:** Incorporates multi-tenant service switcher and account settings as defined in **Company Document**.

## 3. Accessibility & Tokens
- **Contrast Ratio:** WCAG AAA compliance (minimum 7:1 for text, 3:1 for graphical UI elements).
- **Touch Targets:** Minimum 48x48px bounding box for all interactive elements.
- **Tokens:** Integrated into design system token repository (`@skokos/tokens`).

## 4. Documentation & Delivery
Component definitions, interactive Figma prototypes, and states (default, hover, active, disabled) have been synced with engineering via Atlas Core Design System repo.
```