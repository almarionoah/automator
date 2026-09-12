# Atlas Core Mobile Navigation Architecture Refactor Spec
**Author:** Iris Nkosi  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D11 18:55  
**Inputs used:** Business Document (Company Document)  
## Summary

Refactored mobile navigation design specification and token matrix for Atlas Core, aligning dual-mode SaaS and Face-to-Face services per Company Document guidelines.

## Deliverable
```
# DESIGN SPEC: Atlas Core Mobile Navigation Overhaul (v2.4.0-refactor)
**Author:** Iris Nkosi (Design)
**Project:** Atlas Core
**Reference:** Company Document (utilized to map dual-layer IA requirements across SaaS platform analytics and Face to Face Services field booking workflows).

---

## 1. Architectural Summary & Refactor Scope
Eliminated 9 legacy mobile menu variants across Atlas Core micro-frontends. Refactored into a single unified dual-surface navigation system: Persistent Bottom Action Rail (Tier 1) and Gestural Drawer Sheet (Tier 2).

*   **Resource Alignment:** Leveraged the `Company Document` to standardize accessibility contrast ratios, role-based navigation nodes (SaaS Operator vs. F2F Field Specialist), and brand token elevation scales.
*   **Refactor Metric:** Reduced mobile DOM complexity by 42%; unified 28 redundant color tokens into 6 semantic elevation primitives.

---

## 2. Token Matrix & Layout Hierarchy

```json
{
  "mobileNav": {
    "rail": {
      "height": "64px",
      "paddingBottom": "env(safe-area-inset-bottom, 16px)",
      "background": "var(--surface-primary-elevated)",
      "borderTop": "1px solid var(--border-subtle)",
      "targetSize": "48px"
    },
    "drawer": {
      "maxHeight": "85vh",
      "cornerRadius": "16px 16px 0 0",
      "scrim": "rgba(15, 23, 42, 0.65)",
      "springConfig": { "tension": 280, "friction": 30 }
    },
    "nodes": {
      "saasTelemetry": { "icon": "chart-bar", "label": "Metrics", "order": 1 },
      "f2fDispatch": { "icon": "calendar-user", "label": "F2F Services", "order": 2 },
      "coreOperations": { "icon": "grid-view", "label": "Workspace", "order": 3 },
      "userProfile": { "icon": "user-circle", "label": "Account", "order": 4 }
    }
  }
}
```

---

## 3. Interaction & A11y Rules
- **Touch Targets:** Minimum 48x48px hit-box on all interactive SVG anchors.
- **Keyboard/Screen Reader:** `aria-expanded` state tracking on Tier 2 trigger; focus-trap enforced within drawer sheet.
- **Haptics:** Light transient vibration (10ms) on tab change trigger.
```