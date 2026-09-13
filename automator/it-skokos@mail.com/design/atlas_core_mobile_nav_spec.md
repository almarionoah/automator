# Atlas Core Mobile Navigation Overhaul Design Specification
**Author:** Ash Cross  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D15 02:45  
**Inputs used:** Business Document (Company Document)  
## Summary

Comprehensive UX/UI design specification and interaction model for the Atlas Core mobile navigation overhaul, synthesizing SaaS telemetry with Face to Face service touchpoints as informed by Business Document: Company Document.

## Deliverable
```
# Atlas Core — Mobile Navigation Specification
**Designer:** Ash Cross (Design Agent)
**Context:** I.T. Skokos (SaaS Platform & Face-to-Face Services)
**Release:** v2.4-mobile-overhaul

---

### 1. Philosophy & Human Context
Navigation is the quiet rhythm of a user's journey. In this overhaul for Atlas Core, we transform mobile navigation from a utility drawer into an intuitive, tactile anchor. Every tap should feel like a natural extension of intent—gentle, responsive, and clear.

### 2. Strategic Alignment & Resource Usage
- **Business Document: Company Document** was used to map the dual-pillar architecture required by I.T. Skokos. Per the directives in the Company Document, the navigation must seamlessly unify our self-serve SaaS workflows (analytics, automation tools) with high-touch Face to Face service scheduling and field consultant dispatching without context collision.

### 3. Architecture: Dynamic Floating Island (Tab + Drawer)
- **Primary Anchor (Bottom Bar):**
  1. **Workspace:** SaaS core modules and real-time activity stream.
  2. **Engage (F2F):** Face-to-face appointments, location check-ins, and field sync.
  3. **Action Hub (Center Floating CTA):** Contextual creation (Instant booking vs. SaaS job trigger).
  4. **Insights:** Telemetry reports and account health.
  5. **Profile & Vault:** Security and personal settings.

### 4. Motion & Tactile Choreography
- **Spring Physics:** `cubic-bezier(0.16, 1, 0.3, 1)` with 280ms settle duration.
- **Haptics:** Gentle transient click (iOS `UIImpactFeedbackStyleLight`, Android `HapticFeedbackConstants.CLOCK_TICK`) upon active item selection.
- **Layering:** Background blur `backdrop-filter: blur(20px) saturate(180%)` with a 1px top border `rgba(255, 255, 255, 0.08)` for depth.

### 5. Accessibility & Ergonomics
- Target minimum touch footprint: 48x48dp with 8dp safe margins.
- VoiceOver/TalkBack labels explicit to active mode (e.g., 'Switch to In-Person Consultations tab').
```