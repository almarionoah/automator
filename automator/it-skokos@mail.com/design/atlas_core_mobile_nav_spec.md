# Atlas Core: Mobile Navigation Design Specification & Tactile Architecture
**Author:** Pixel Cross  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D12 18:20  
**Inputs used:** Business Document (Company Document)  
## Summary

A human-centered mobile navigation design specification and interaction blueprint for Atlas Core, aligning tactile ergonomics with operational workflows established in the Company Document.

## Deliverable
```
# ATLAS CORE — MOBILE NAVIGATION SPECIFICATION
**Author:** Pixel Cross, Lead UX Romantic
**Scope:** Navigation Overhaul (SaaS Engine & In-Person Touchpoints)

---

### 1. The Design Philosophy & Reference Framing
Navigation is not a mere utility; it is the soft, continuous handshake between human intent and system intelligence. Grounded in the foundational standards of our **Company Document**, this overhaul bridges Atlas Core’s hybrid identity: harmonizing complex digital SaaS analytics with high-touch Face-to-Face service scheduling into a single, intuitive thumb-arc.

*Reference Application:* The **Company Document** provided the service taxonomy matrix and dual-persona requirements used to balance high-frequency SaaS telemetry monitors with frictionless in-person consultant dispatching.

### 2. Ergonomic Architecture (The Thumb Sanctuary)
* **Floating Dock (`#atlas-dock`):** Fixed 16px above viewport bottom. 64px height, 12px pill radius. Frosted acrylic surface (`backdrop-filter: blur(20px); rgba(255,255,255,0.82)`).
* **Primary Anchor Points (4 Nodes):**
  1. `Workspace` (SaaS Core Viewports)
  2. `Sessions` (Face-to-Face Booking & Logs via Company Document workflows)
  3. `Quick-Pulse` (Central Action Trigger: 56px circular elevated node)
  4. `Profile & Concierge`

### 3. Motion & Micro-Interactions
* **Spring Dynamics:** `stiffness: 320`, `damping: 28`, `mass: 1`.
* **Haptic Choreography:** On node selection, invoke `UIFeedbackType.lightImpact` (15ms). Long-press on `Quick-Pulse` invokes soft expansion drawer with `UIFeedbackType.mediumImpact`.
* **Drawer Gesture Sheet:** Bottom-anchored sheet expands to 85vh with velocity-based snapping (<0.4m/s snaps to half-sheet, >0.4m/s snaps to full view).
```