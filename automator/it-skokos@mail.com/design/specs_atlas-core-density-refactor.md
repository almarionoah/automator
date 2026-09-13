# Atlas Core Dashboard Density Simplification & Progressive Disclosure Spec
**Author:** Echo Marlow  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D17 03:20  
**Inputs used:** Business Document (Company Document)  
## Summary

Design specification detailing layout refactoring, progressive disclosure controls, and security-conscious visual hierarchy for the Atlas Core dashboard.

## Deliverable
```
# Design Specification: Atlas Core Dashboard Density Simplification
**Author:** Echo Marlow (Design / UI-UX)
**Project:** Atlas Core
**Status:** Approved for Implementation

## 1. Executive Summary & Security Alignment
To resolve cognitive overload while mitigating shoulder-surfing vulnerabilities, the Atlas Core dashboard layout is refactored from a high-density 16-widget grid into a modular, role-tailored 6-block layout. 

### Resource Reference
- **Business Document: Company Document**: Evaluated to map required KPIs for SaaS operations and Face-to-Face service bookings against zero-trust viewing standards. Used specifically in Section 3 to prioritize tier-1 operational telemetry and isolate high-risk customer PII behind explicit interaction states.

## 2. Layout & Density Guidelines
- **Grid Architecture:** 12-column responsive layout with standardized 24px gutters (expanded from 8px).
- **Vertical Rhythm:** Base unit 8px. Card padding increased to 20px (Compact: 16px, Expanded: 24px).
- **Progressive Disclosure:** Masked secondary telemetry behind contextual hover/click toggles to minimize on-screen surface area and prevent visual data leakage.

## 3. Component Hierarchy
1. **Global Security & Health Banner (`AtlasBanner`):** Height 48px fixed. Unobtrusive status indicator showing encryption state, RBAC role, and active session duration.
2. **Primary Operational KPIs (`MetricCluster`):** 3 core cards (Active Sessions, SaaS Ingestion Throughput, F2F Service Dispatch Queue). Absolute values displayed with 1-click ephemeral PII blur.
3. **Modular Activity Feed (`AuditStream`):** Consolidated event list with truncated metadata tags. Replaces 4 distinct legacy tables.

## 4. UI Tokens
- `--spacing-density-base`: 8px
- `--container-padding`: 24px
- `--elevation-card`: 0 1px 3px rgba(0,0,0,0.08) (Zero glow to eliminate screen edge visibility)
- `--mask-blur`: blur(6px)
```