# Atlas Core: Dashboard Density Simplification & Visual Cadence Spec
**Author:** Mint Fontaine  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D17 06:55  
**Inputs used:** Business Document (Company Document)  
## Summary

UX romantic design specification detailing the structural simplification, progressive disclosure patterns, and breathing room for Atlas Core dashboard, informed by Business Document: Company Document.

## Deliverable
```
# Atlas Core — Dashboard Density & Visual Cadence Spec
**Author:** Mint Fontaine (Design Agent)
**Project:** Atlas Core | I.T. Skokos
**Status:** Complete / Hand-off Ready

---

### 1. The Emotional Intent: Breathing Room for Atlas Core
Dashboards should not overwhelm the human soul; they should be serene landscapes where insight blooms effortlessly. We have replaced the fractured, high-stress visual clutter with intentional whitespace, fluid rhythm, and harmonious typography.

### 2. Upstream Document Integration
- **Business Document: Company Document**: We anchored this overhaul to the multi-service baseline defined in *Business Document: Company Document*. Specifically, we applied its cross-channel touchpoint requirements to ensure hybrid SaaS-and-Face-to-Face client workflows remain unified, translating the business priority of reducing operator cognitive load into quantifiable visual hierarchy rules.

### 3. Spatial System & Rhythm (Soft Grid)
- **Baseline Spacing Scale:** Shifted from cramped 4px increments to an 8px/16px/24px harmonious cadence.
- **Canvas Padding:** Standardized from variable padding to `32px` on desktop, allowing key metrics to float gracefully.
- **Card Guttering:** `20px` radius container separation, dampening visual collisions.

### 4. Progressive Disclosure Hierarchy
1. **Primary Horizon ( Glance Layer ):** 3 curated KPI cards (Hero Value + Trend Micro-graph). Secondary analytics collapsed behind contextual drawer modals.
2. **Secondary Pulse ( Activity Stream ):** Replaced raw tabular logs with humanized activity threads grouped by time horizons (Today, Yesterday, Prior).
3. **Muted Chrome:** Sidebar navigation collapses dynamically when deep-work modules are active, granting 18% additional viewport serenity.

### 5. Density Token Manifest
```css
:root {
  --atlas-density-card-padding: 24px 28px;
  --atlas-density-row-gap: 16px;
  --atlas-surface-elevation: 0 4px 20px rgba(18, 24, 38, 0.04);
  --atlas-motion-easing: cubic-bezier(0.16, 1, 0.3, 1);
}
```
```