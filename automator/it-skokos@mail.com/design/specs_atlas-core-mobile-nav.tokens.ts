# Atlas Core: Refactored Mobile Navigation Architecture & Token Spec
**Author:** Volt Nkosi  
**Department:** Design  
**Project:** Atlas Core  
**Produced:** D12 02:25  
**Inputs used:** Business Document (Company Document)  
## Summary

Complete mobile navigation overhaul for Atlas Core, refactoring the bottom navigation matrix, drawer primitives, and touch targets to harmonize SaaS tooling with Face-to-Face service scheduling, derived directly from the Business Document: Company Document.

## Deliverable
```
/**
 * ATLAS CORE — MOBILE NAVIGATION REFACTOR v2.4.0
 * Author: Volt Nkosi (Design)
 * Style: Obsessive modular refactoring & atomic token alignment.
 * 
 * Upstream Reference:
 * - 'Business Document: Company Document': Applied Section 3.2 (Service Parity Guidelines) 
 *   to unify SaaS dashboard telemetry with offline Face-to-Face appointment dispatch
 *   within a persistent 4-slot thumb-zone navigation matrix.
 */

export const AtlasMobileNavTokens = {
  geometry: {
    barHeight: '64px',
    safeAreaBottom: 'env(safe-area-inset-bottom, 16px)',
    hitTargetMin: '48px',
    iconSize: '24px',
    activeIndicatorHeight: '3px',
    drawerMaxHeightRatio: 0.85,
  },
  zIndex: {
    navBar: 1100,
    sheetOverlay: 1200,
    sheetContent: 1250,
    toastBoundary: 1300,
  },
  motion: {
    sheetEnter: 'cubic-bezier(0.16, 1, 0.3, 1) 320ms',
    sheetExit: 'cubic-bezier(0.7, 0, 0.84, 0) 200ms',
    tabTransition: 'cubic-bezier(0.2, 0, 0, 1) 180ms',
  }
} as const;

export interface NavItem {
  id: 'saas_analytics' | 'f2f_sessions' | 'dispatch_map' | 'account_hub';
  label: string;
  route: string;
  badgeKey?: string;
}

// Refactored from legacy 7-item overflow to 4 primary anchors + unified Drawer
export const PRIMARY_NAV_ITEMS: readonly NavItem[] = [
  {
    id: 'saas_analytics',
    label: 'Platform',
    route: '/core/platform',
  },
  {
    id: 'f2f_sessions',
    label: 'F2F Bookings',
    route: '/services/face-to-face',
    badgeKey: 'pending_client_signoffs',
  },
  {
    id: 'dispatch_map',
    label: 'Field Ops',
    route: '/dispatch/active',
  },
  {
    id: 'account_hub',
    label: 'Atlas Hub',
    route: '/hub/overview',
  },
] as const;

export const DrawerActionHierarchy = {
  groupA: 'SaaS Telemetry & Tenant Switcher',
  groupB: 'Face-to-Face Route Optimization & Local Check-in',
  groupC: 'Support Escalation & Offline Sync State',
} as const;
```