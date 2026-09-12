# Atlas Core - Dashboard Density Simplification & Visual Security Architecture
**Author:** Prism Ito  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D12 07:55  
**Inputs used:** Business Document (Company Document)  
## Summary

Design specification establishing relaxed spatial tokens, progressive disclosure patterns, and zero-leakage visual sanitization protocols for the Atlas Core dashboard.

## Deliverable
```
# Design Specification: Atlas Core Dashboard Density Redesign (v2.4.0-SEC)
**Author:** Prism Ito, Design Lead
**Project:** Atlas Core | I.T. Skokos
**Security Posture:** High / Threat-Informed UX

## 1. Context & Resource Integration
This specification re-architects the Atlas Core dashboard from a dense 4px micro-grid to an 8px defensive macro-structure. The goal is twofold: dramatically reduce cognitive fatigue and mitigate physical visual eavesdropping (shoulder-surfing / accidental screen capture).
- **Company Document**: Explicitly utilized to cross-reference data sensitivity tiers against visual display thresholds, ensuring tenant-specific SaaS metrics and Face to Face service logs comply with mandatory separation and masking standards.

## 2. Layout Token System (Relaxed Grid)
We eliminate raw information flooding by enforcing strict layout limits:
- `$surface-padding`: 24px (expanded from 12px)
- `$component-gap`: 16px (expanded from 6px)
- `$max-primary-widgets`: Hard limit of 6 KPI cards in primary viewport (2x3 responsive grid).
- `$elevation-treatment`: Hard boundary 1px `#1E293B` borders replacing ambient glow to prevent visually ambiguous data overlap.

## 3. Defensive Progressive Disclosure & Masking
- **Default-Masked Telemetry**: Confidential financial and tenant identity fields render masked by default (`filter: blur(5px)` with synthetic skeleton placeholders).
- **Intent-Based Revealing**: Cleartext values require explicit cursor dwell (>250ms) with a visual active-state border.
- **Ephemeral Reveal Timeout**: Unmasked fields automatically revert to masked state after 8 seconds of idle pointer time.

## 4. Viewport Architecture
1. **Top Status Rail (64px)**: High-priority operational health indicators only.
2. **Primary Metric Grid**: 6 low-cognitive-load summaries with trend arrows.
3. **Drawer Inspection**: Deep log analysis moved out of main view into isolated modal panels.
```