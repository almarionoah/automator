# Atlas Core UI Refactor: Secure Dashboard Density Simplification Spec
**Author:** Jax Ito  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D18 12:25  
**Inputs used:** Business Document (Company Document)  
## Summary

Design specification for reducing visual cognitive load and dashboard density in Atlas Core while enforcing zero-trust UI data masking and strict RBAC progressive disclosure rules.

## Deliverable
```
# UI/UX Specification: Atlas Core Dashboard Density Simplification
Author: Jax Ito (Design Agent)
Project: Atlas Core | I.T. Skokos Platform
Security Tier: Confidential / Zero-Trust UI

## 1. Context & Governance
Following the UX audit of the Atlas Core dashboard, information density presented significant cognitive friction and visual vulnerability (risk of shoulder surfing / unauthorized screen capture in hybrid environments). In accordance with the guidelines established in **Business Document: Company Document**, visual information architecture has been aligned with strict data classification tiers and least-privilege layout rules.

## 2. Density Reductions & Layout Refactoring
- **Grid Architecture**: Transitioned from 6-column dense widget matrix to an 8pt modular 3-column layout. Max canvas width: 1440px centered.
- **Vertical Rhythm**: Standardized card padding to `spacing-lg` (24px) from variable 8px/12px padding.
- **Progressive Disclosure**: Consolidated 14 real-time micro-charts into 4 macro KPI health tiles with secondary telemetry nested inside drill-down panels.

## 3. Security-First Visual Hardening
- **Default Masking State**: In alignment with **Business Document: Company Document**, all PII, client names, and face-to-face service location metadata default to redacted obfuscation glyphs (`██████`) unless active role-based permission (Level 3+) and user focus are verified.
- **Anti-Screen Capture Rendering**: Render sensitive metric values using SVG path hashing rather than plaintext DOM nodes where feasible to mitigate client-side scraper exposure.
- **Audit Visibility**: Added persistent, low-profile watermarking and session integrity badges in the sub-header.

## 4. Component Token Adjustments
- `surface-elevation-1`: `#0F172A` (Card background, 1px border `#1E293B`)
- `spacing-widget-gap`: `24px` (previously `8px`)
- `text-metric-primary`: `32px` / `line-height: 40px` / `font-weight: 600`
- `state-redacted-fill`: `#334155` with blurred backdrop filter
```