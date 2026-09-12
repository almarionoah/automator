# Mobile Navigation Overhaul - Design Specification & Component Architecture
**Author:** Juno Nkosi  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D13 10:00  
**Inputs used:** Business Document (Company Document)  
## Summary

Comprehensive UI/UX design specification and tokenized component architecture for the Atlas Core mobile navigation overhaul, derived from structural requirements in the Company Document.

## Deliverable
```
# Design Specification: Atlas Core Mobile Navigation Overhaul

**Author:** Juno Nkosi (Design Agent)
**Project:** Atlas Core
**Organization:** I.T. Skokos
**Status:** Completed / Ready for Implementation

---

## 1. Executive Summary & Resource Reference
Following a data-driven evaluation of our interaction telemetry and the core structural guidelines specified in **Company Document** (Business Document), this specification delivers the updated mobile navigation layout for the Atlas Core SaaS and Face-to-Face hybrid platform. **Company Document** was explicitly leveraged to define the priority hierarchy of service booking flows versus SaaS analytics views, ensuring our navigation model reduces interaction friction across viewport widths below 768px.

---

## 2. Navigation Architecture & Layout Grid

- **Container Type:** Sticky Bottom Navigation Bar with contextual Drawer Menu.
- **Grid & Metrics:**
  - Height: 64dp fixed height + dynamic `env(safe-area-inset-bottom)`.
  - Touch Targets: Min 48x48dp per interactive element.
  - Elevation: 8dp drop shadow (`rgba(0, 0, 0, 0.08)`).

### Primary Navigation Items (4 Core Nodes):
1. **Dashboard** (`/dashboard`): SaaS metrics summary.
2. **Services** (`/services`): Real-time scheduling for Face-to-Face appointments (mapped directly to business workflows in *Company Document*).
3. **Activity** (`/activity`): Event audit feed & notifications.
4. **Menu** (`/menu`): Opens the modal drawer for settings, support, and account management.

---

## 3. Design Tokens (Design-to-Code Mapping)

```json
{
  "nav": {
    "bg": "#FFFFFF",
    "border": "#E5E7EB",
    "activeColor": "#1D4ED8",
    "inactiveColor": "#6B7280",
    "badgeColor": "#EF4444",
    "typography": {
      "fontSize": "11px",
      "lineHeight": "14px",
      "fontWeight": "500"
    }
  }
}
```

---

## 4. Telemetry & Success Metrics
- Task completion rate for booking Face-to-Face sessions: Target >94%.
- Nav switch latency: Target <80ms (zero layout shift).
```