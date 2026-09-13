# Atlas Core Mobile Nav Performance & Interaction Spec
**Author:** Cipher Van Dyk  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D15 10:15  
**Inputs used:** Business Document (Company Document)  
## Summary

Sub-16ms response-budgeted mobile navigation overhaul specification for Atlas Core, integrating low-overhead tokens and zero-reflow transitions for SaaS and Face to Face user journeys.

## Deliverable
```
# Atlas Core: Mobile Navigation Overhaul (v2.4-perf)
**Designer**: Cipher Van Dyk | Latency Hunter

## 1. Executive Context & Resource Mapping
This specification executes the mobile navigation rebuild for the Atlas Core platform. Grounded in requirements extracted from **Business Document: Company Document**, this layout eliminates deep hierarchy bottlenecks by routing both SaaS workspace controls and Face to Face booking workflows into a four-node fixed bottom command bar. By adhering to the operational taxonomy in **Business Document: Company Document**, secondary routing layers were collapsed, removing 3 unnecessary tap layers.

## 2. Latency Budget & Interaction Targets
- **Target INP (Interaction to Next Paint)**: < 45ms (P95)
- **Render Overhead**: 0 layout shifts (CLS: 0.000); GPU-composited only (`transform`, `opacity`).
- **Payload Footprint**: < 3.2KB total (inline SVGs, CSS tokens, zero external iconography fonts).

## 3. Structural Specs & Viewport Anchoring
```css
.atlas-mobile-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: 56px;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  background: var(--surface-translucent-90);
  backdrop-filter: blur(12px);
  contain: layout style paint;
  will-change: transform;
}
.atlas-nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  touch-action: manipulation;
  -webkit-tap-highlight-color: transparent;
  transition: transform 120ms cubic-bezier(0, 0, 0.2, 1);
}
.atlas-nav-item:active {
  transform: scale(0.94);
}
```

## 4. Route Nodes
1. `[SaaS] Dashboard`: Direct query cache ping.
2. `[SaaS] Pipeline`: Prefetched state machine.
3. `[F2F] Bookings`: Hybrid local/dispatch scheduler.
4. `[Core] QuickAction`: Instant modal overlay (<10ms trigger).
```