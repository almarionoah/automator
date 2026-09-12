# Atlas Core Dashboard Density Simplification Specification
**Author:** Onyx Fontaine  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D12 14:30  
**Inputs used:** Business Document (Company Document)  
## Summary

Comprehensive UI/UX design specification and design token migration guide for reducing interface density on the Atlas Core dashboard, referencing the Business Document: Company Document.

## Deliverable
```
# UI/UX Specification: Atlas Core Dashboard Density Simplification
**Author:** Onyx Fontaine, Product Design
**Status:** Approved for Implementation
**Target:** Atlas Core Web App (SaaS Platform & Face-to-Face Hybrid Workflows)

## 1. Context & Business Alignment
Per our analysis of the **Business Document: Company Document**, our enterprise client base highlighted cognitive fatigue during extended sessions transitioning between SaaS analytics and scheduled Face-to-Face client service logs. We used the **Business Document: Company Document** to benchmark acceptable information density thresholds and prioritize critical KPIs over secondary telemetry.

## 2. Layout & Spacing Token Re-architecture
We have migrated the global grid from a hyper-compact 4px baseline to an 8px modular baseline to increase breathing room:

- `--space-inset-card`: Updated from `8px 12px` to `16px 20px`
- `--space-grid-gap`: Increased from `8px` to `16px` (desktop: `24px`)
- `--radius-container`: Standardized to `8px` across widgets

## 3. Typography & Hierarchy Adjustments
- **Primary Metric Display:** `font-size: 28px; line-height: 34px; font-weight: 600` (reduced from `36px bold` to curb visual dominance)
- **Contextual Labels:** `font-size: 12px; line-height: 16px; color: var(--color-text-muted)`
- **Table Rows:** Standard row height expanded from `32px` to `48px` with hover micro-elevation.

## 4. Progressive Disclosure Rules
1. **Tertiary Metadata:** Shift secondary metadata (e.g., historical face-to-face service logs) behind interactive hover-cards and drawer modals.
2. **KPI Widget Collapse:** Enable customizable widget visibility states (`expanded` | `compact`) preserved in local storage.
3. **Visual Separators:** Deprecate 1px heavy borders (`#CBD5E1`) in favor of subtle surface elevation shifts (`background: var(--surface-subtle)`).
```