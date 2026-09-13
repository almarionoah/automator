# Atlas Core: Mobile Navigation Overhaul Design Specification
**Author:** Kilo Okafor  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D15 13:30  
**Inputs used:** Business Document (Company Document)  
## Summary

UX interaction spec and emotional design choreography for the revamped Atlas Core mobile navigation bar, bridging digital workflows and face-to-face service access.

## Deliverable
```
# Design Specification: Atlas Core Mobile Navigation Overhaul
Author: Kilo Okafor (UX Design)
Project: Atlas Core | I.T. Skokos

## 1. Intent & Emotional Resonance
Navigation is the pulse of user autonomy. This overhaul transforms Atlas Core's mobile drawer into a tactile, floating glass dock that breathes with user motion. We bridge digital SaaS tooling with our face-to-face service touchpoints through rhythmic haptics, seamless gesture curves, and contextual elevation.

## 2. Strategic Alignment & Resource Integration
- **Business Document: Company Document**: We anchored this overhaul to the cross-surface hierarchy established in `Company Document`, adopting its defined service matrix (SaaS workspace vs. Face-to-Face appointment coordination) to streamline high-velocity actions into the primary bottom bar while tucking secondary enterprise tooling into an organic thumb-reach overlay.

## 3. Component Architecture & Motion Choreography

### A. Floating Dock (Bottom Tier)
- **Container**: `backdrop-filter: blur(24px) saturate(180%)`; Border: `1px solid rgba(255, 255, 255, 0.12)`; Radius: `32px`.
- **Elevation**: Ambient shadow `0 12px 32px -4px rgba(15, 23, 42, 0.16)`.
- **Tabs (4 slots)**:
  1. Core Workspace (SaaS dashboard)
  2. F2F Engagements (Live booking & physical check-in tracker)
  3. Quick Action Hub (Center elevated FAB: 'Connect & Orchestrate')
  4. Profile & Knowledge Matrix

### B. Micro-Interactions & Gestures
- **Tab Switch**: Spring physics (`stiffness: 380, damping: 28`). Active indicator glides beneath icon with a 4ms subtle haptic tap (UIFeedbackType.lightImpact).
- **F2F Dynamic Pill**: Real-time status badge pulse (`#10B981`, 2.4s ease-in-out glow) when an in-person session is within a 2-hour window.

## 4. Accessibility & Spatial Compliance
- Minimum tap target: `48x48dp` with 12dp safety padding.
- Dynamic Type scaling up to 200% with horizontal overflow failover.
- Full WCAG 2.1 AAA contrast ratio across Light and Nocturne palettes.
```