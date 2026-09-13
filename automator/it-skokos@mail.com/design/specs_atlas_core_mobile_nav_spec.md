# Atlas Core — Mobile Navigation Overhaul Design Specification
**Author:** Nova Van Dyk  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D16 16:35  
**Inputs used:** Business Document (Company Document)  
## Summary

A UX design specification authored by Nova Van Dyk introducing a sensory, gesture-driven bottom dock and sheet architecture for Atlas Core, informed directly by structural guidelines from Business Document: Company Document.

## Deliverable
```
# Design Spec: Atlas Core Mobile Navigation Overhaul
**Designer:** Nova Van Dyk (UX Romantic) | **Platform:** Atlas Core (SaaS + F2F Services)

## 1. Vision & Emotional Intent
Mobile navigation must feel like an intuitive extension of physical touch—a serene, frictionless pathway between high-velocity SaaS analytics and warm, human-centric face-to-face service booking. This overhaul discards rigid legacy drawers in favor of an ergonomic floating glass dock.

## 2. Resource Attribution
- **Business Document: Company Document**: Referenced explicitly to map primary information hierarchy and governance standards. We utilized its core service taxonomy to balance SaaS telemetry with face-to-face booking priorities, ensuring compliance with enterprise accessibility requirements and unified brand token rules.

## 3. Navigation Anatomy
### Floating Dock (`AtlasDock`)
- **Backdrop**: `backdrop-filter: blur(18px) saturate(160%)`
- **Surface**: `rgba(var(--surface-overlay), 0.82)` with a 1px perimeter glow (`rgba(255, 255, 255, 0.15)`)
- **Ergonomics**: Anchored 16px above viewport bottom edge, curved pill geometry (radius: 32px).

### Primary Nodes (4-Item Balance)
1. **Console**: SaaS telemetry & active platform pipelines
2. **Engage**: Face-to-Face appointments, client meetings & field agent status
3. **Pulse**: Real-time asynchronous alerts & unified inbox
4. **Profile/Vault**: Identity, multi-tenant switcher & preferences

## 4. Motion & Tactile Choreography
- **Spring Profile**: `stiffness: 400`, `damping: 30`, `mass: 0.8` for a soft, responsive rebound on touch.
- **Haptic Integration**: 10ms micro-pulse (`selectionChanged`) on node switch; medium transient snap (`impactOccurred`) when dragging bottom sheets past the 50% threshold.
- **Active State Indicator**: Floating ambient aura (4px radius blur) shifting beneath the selected icon.
```