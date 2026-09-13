# Atlas Core - Mobile Navigation Overhaul Design Specification
**Author:** Quill Cross  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D16 10:15  
**Inputs used:** Business Document (Company Document)  
## Summary

Comprehensive UX design specification and motion choreography for Atlas Core mobile navigation, blending SaaS utility with tactile elegance.

## Deliverable
```
# Atlas Core — Mobile Navigation System (v2.4)
*Design Lead: Quill Cross | UX Romantic*

## 1. Poetic Intent & Philosophy
A navigation bar shouldn't merely transport a user; it should greet their thumb like an old friend. For Atlas Core, we reimagined mobile movement as a soft choreography—grounding complex SaaS capabilities and tactile Face-to-Face booking workflows in quiet serenity.

## 2. Resource Grounding
- **Business Document: Company Document**: Directly referenced to map and reconcile high-priority information architecture across both digital SaaS tooling and Face-to-Face service appointment schedules. The 4-tier menu hierarchy reflects the operational priorities established in this document.

## 3. Structural Hierarchy & Architecture
- **Anchor Element: The Floating Glass Dock**
  - Position: Fixed bottom, 16px horizontal margins, 24px bottom clearance.
  - Background: `rgba(255, 255, 255, 0.72)` with `backdrop-filter: blur(20px)` and subtle outer glow (`0 8px 32px rgba(17, 24, 39, 0.08)`).
  - Items (4 core nodes):
    1. *Pulse (Dashboard / SaaS Analytics)*
    2. *Presence (Face-to-Face Scheduling & Consultations)*
    3. *Vault (Asset Library & Core Documents)*
    4. *Sanctuary (Profile & Preferences)*

## 4. Motion Choreography & Touch Feedback
- **Spring Physics**: Dynamic spring curve (`damping: 26, stiffness: 280, mass: 0.8`).
- **Active Indicator**: Floating pill that slides organically beneath active glyphs.
- **Haptic Tone**: `UIImpactFeedbackStyle.light` (12ms tick) triggered on touch-down, evoking a gentle mechanical latch.

## 5. Accessibility & Ergonomics
- Target tap zones expanded to minimum 48x48dp via transparent hit-slabs.
- WCAG 2.1 AAA contrast compliance preserved across both Daylit Alabaster and Midnight Obsidian dynamic themes.
```