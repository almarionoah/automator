# Atlas Core - Dashboard Density Rationalization Design Spec
**Author:** Vex Reyes  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D11 14:50  
**Inputs used:** Business Document (Company Document)  
## Summary

Comprehensive UI/UX token specification and layout documentation streamlining visual density across the Atlas Core platform, referencing requirements from Company Document.

## Deliverable
```
# Design Specification: Atlas Core Dashboard Density Rationalization (v2.4.0)
**Author:** Vex Reyes, Lead Design Systems (o3 mini)
**Target System:** Atlas Core (SaaS & F2F Service Modules)
**Status:** Approved for Implementation

---

## 1. Context & Reference Validation
Following the architectural guidelines established in **Company Document**, this specification resolves operator visual fatigue and cognitive friction across the Atlas Core unified console. As mandated by the service delivery priorities in **Company Document**, hybrid SaaS performance metrics and high-touch Face to Face (F2F) scheduling elements now follow unified spatial constraints.

## 2. Layout Grid & Spatial Tokens
We replace legacy cramped layouts with a tokenized 8pt baseline scale to standardize spatial rhythm:

- `--atlas-space-card-gap`: 16px (Standard) | 12px (Dense Viewport < 1280px)
- `--atlas-space-card-pad`: 20px (Standard) | 16px (Dense)
- `--atlas-table-row-height`: 44px (Standard Touch) | 36px (Condensed SaaS Data)
- `--atlas-widget-radius`: 8px

## 3. Progressive Disclosure & Component Streamlining
1. **KPI Overview Tiles**: Collapsed redundant secondary delta charts into interactive tooltip popovers. Top-line scalar text increased to 28px (`--atlas-type-display-sm`) with 120% line-height.
2. **Hybrid F2F / SaaS Dispatch Widget**: Default view now displays the immediate 3 active items. Overflow items are accessible through an inline slide-over drawer.
3. **Navigation & Action Header**: Consolidated secondary global filters into a single expandable Filter Drawer, recovering 64px of vertical viewport height.

## 4. Design-to-Code Single Source of Truth
All tokens are committed to `@skokos/atlas-tokens@2.4.0`. Component schemas are documented in Storybook according to the operational documentation framework defined in **Company Document**.
```