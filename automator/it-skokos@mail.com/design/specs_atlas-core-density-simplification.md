# Atlas Core Dashboard Density & Privacy Layout Specification
**Author:** Ash Petrov  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D15 01:55  
**Inputs used:** Business Document (Company Document)  
## Summary

Design specification refactoring Atlas Core's dashboard to eliminate visual clutter, optimize layout hierarchy, and enforce security-first progressive disclosure and privacy masking based on business requirements.

## Deliverable
```
# UI/UX Specification: Atlas Core Dashboard Density & Privacy Optimization
**Author:** Ash Petrov (UI/UX Design)
**Project:** Atlas Core
**Security Classification:** Confidential / Security-Hardened

## 1. Resource References & Usage
- **Business Document: Company Document**: Utilized to audit mandatory business KPI requirements against face-to-face operational workflows. This ensured secondary telemetry could be safely moved behind progressive disclosure without violating corporate governance or core reporting standards.

## 2. Problem Statement & Threat Vector
The legacy Atlas Core dashboard suffered from severe information density (42 visible metrics/tiles on 1080p). In addition to cognitive overload, this high-density layout introduced critical security liabilities (shoulder-surfing risk during Face-to-Face client consultations and excessive sensitive telemetry exposed in unmasked DOM elements).

## 3. Layout & Density Guidelines
- **Grid Architecture**: Shifted from 4px compact micro-grid to a hardened 8px/16px baseline layout.
- **Card Reduction**: Primary viewport restricted to 4 vital telemetry cards (Active Services, System Health, Auth Rate, SLA Thresholds).
- **Progressive Disclosure**: Secondary audit logs and granular node diagnostics moved to collapsed drawer overlays requiring explicit user intent.

## 4. Security-Hardened UI Tokens & Controls
- **Masked-by-Default Tokens**: Sensitive KPI counters, account IDs, and PII render with CSS mask blur (`filter: blur(5px)`) and backend-level string redaction until explicit hover/unlock.
- **DOM Sanitization Boundary**: UI elements prevent raw payload storage in `data-*` attributes.
- **Face-to-Face Presentation Mode**: A single-click toggle instantly strips tenant-specific metadata and financial metrics when running Atlas Core during client-facing meetings.
```