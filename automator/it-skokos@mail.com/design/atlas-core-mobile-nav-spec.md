# Atlas Core: Mobile Navigation Overhaul Design Specification
**Author:** Nova Bishop  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D13 03:40  
**Inputs used:** Business Document (Company Document)  
## Summary

A UX romantic design specification detailing the tactile architecture, choreography, and emotional resonance of the Atlas Core mobile navigation system, aligning digital SaaS workflows with face-to-face services.

## Deliverable
```
# Design Specification: Atlas Core Mobile Navigation Overhaul
*Lead Designer: Nova Bishop | Style: UX Romantic | Project: Atlas Core*

## 1. Vision & Emotional Architecture
Mobile navigation should feel like an intuitive extension of physical touch—a serene transition between SaaS productivity and warm, face-to-face service facilitation. This overhaul replaces rigid drawers with a floating, thumb-ergonomic glass bar that responds harmoniously to user intent.

## 2. Institutional Alignment
- **Business Document: Company Document**: Directly referenced to restructure primary information architecture. We mapped the foundational service taxonomy and hybrid delivery models defined in the Company Document into a unified 4-node mobile continuum: Dashboard (SaaS), Engagements (F2F Booking & Status), Intelligence (Atlas Insights), and Atelier (Account & Profile).

## 3. Interaction Choreography & Motion Design
- **Bottom Floating Dock**: Height: 64dp, Margin: 16dp float from base. Background: `rgba(255, 255, 255, 0.85)` with `backdrop-filter: blur(20px)` and gentle border glow `rgba(45, 55, 72, 0.08)`.
- **Active Node Indicator**: Spring physics with organic damping (`stiffness: 320, damping: 28`). A soft pill of light glides under the selected icon.
- **Haptic Feedback**: Micro-impact (`light_tick`, 15ms) on touch down; soft release on state confirmation.
- **Sheet Transitions**: Upward velocity translates to an ease-out cubic curve (`cubic-bezier(0.16, 1, 0.3, 1)`), opening face-to-face schedule modals without jarring the context.

## 4. Accessibility & Human Ergonomics
- Thumb-zone optimized: 92% of critical interactive targets sit inside the natural sweeping arc.
- Dynamic Type scaled: Base 11pt captions scale up to 14pt without clipping dock geometry.
```