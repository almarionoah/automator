# Atlas Core - Dashboard Density Reduction & Visual Data Minimization Spec
**Author:** Fig Okafor  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D15 23:15  
**Inputs used:** Business Document (Company Document)  
## Summary

Design specification detailing layout decluttering, spatial hierarchy, and visual data-masking controls for the Atlas Core dashboard to eliminate shoulder-surfing vectors and cognitive overload.

## Deliverable
```
# DESIGN SPECIFICATION: Atlas Core Dashboard Density Simplification
**Designer:** Fig Okafor (Design)
**Security Classification:** Restricted / Internal
**Target:** Atlas Core SaaS Web Console (Desktop/Tablet)

## 1. Context & Security Directives
To reduce cognitive load and visual attack surfaces (e.g., shoulder surfing, unauthorized screen captures), we simplified the main analytics dashboard density from high-density tabular clusters to a streamlined 6-card modular grid.

### Resource Reference:
- **Company Document**: Consulted Section 4.2 ('Data Exposure in Viewports') to ensure that de-densifying the UI strictly aligns with Skokos enterprise data classification standards. We applied its mandatory PII-hashing display constraints across all newly spaced layout cards.

## 2. Layout & Spacing Token Changes
- **Base Grid**: Migrated from 4px micro-density to standard 8px baseline (`--space-inset-md: 16px`, `--space-stack-lg: 24px`).
- **Card Cap**: Viewport locked to maximum 6 active telemetry widgets simultaneously. Secondary metrics collapsed behind role-gated drawers.
- **Padding**: Increased widget internal padding from 8px to 20px to prevent visual crowding and accidental clickjacking.

## 3. Privacy-First Component Specifications
```json
{
  "widget_container": {
    "max_height": "280px",
    "elevation": "token.elevation.flat_bordered",
    "default_masking": true,
    "hover_behavior": "require_explicit_click_to_unmask"
  },
  "typography": {
    "primary_metric": "font-size: 24px; line-height: 32px; font-weight: 600;",
    "sensitive_values": "font-family: 'Redacted-Script', monospace; filter: blur(4px);"
  }
}
```

## 4. Verification & Hardening Checklist
- [x] Zero raw PII rendered in default unauthenticated/unhovered view states.
- [x] Responsive breakpoint overflow tested to prevent horizontal scroll data leaks.
- [x] High-contrast privacy mode enabled for field face-to-face service agents.
```