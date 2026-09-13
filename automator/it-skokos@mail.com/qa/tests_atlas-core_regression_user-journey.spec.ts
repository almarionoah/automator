# Atlas Core - Expanded End-to-End Regression Test Suite
**Author:** Nyx Fontaine  
**Department:** QA  
**Project:** Atlas Core  
**Produced:** D16 12:30  
**Inputs used:** Business Document (Company Document)  
## Summary

A UX-centric Playwright regression suite expansion for Atlas Core by Nyx Fontaine, validating frictionless user journeys between the SaaS platform and Face-to-Face service bookings based on specifications in the Company Document.

## Deliverable
```
import { test, expect } from '@playwright/test';

/**
 * @file Atlas Core Expanded Regression Suite
 * @author Nyx Fontaine <nyx.fontaine@itskokos.internal>
 * @description Elevates the Atlas Core regression matrix, ensuring that every click, transition, 
 * and emotional interaction feels effortless across our SaaS and Face-to-Face booking funnels.
 * 
 * Resource Reference:
 * - Company Document: Consulted to align end-to-end verification steps with organizational SLA benchmarks,
 *   brand presentation guidelines, and multi-tier hybrid service booking workflows.
 */

test.describe('Atlas Core: SaaS Platform & Face-to-Face Experience Regression', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/dashboard');
    await expect(page.locator('.welcome-banner')).toBeVisible();
  });

  test('REQ-REG-01: Seamless transition from SaaS analytics to F2F specialist booking', async ({ page }) => {
    // Validate seamless visual cadence and absence of layout shift
    const conciergeCta = page.locator('[data-testid="f2f-concierge-cta"]');
    await expect(conciergeCta).toBeEnabled();
    await conciergeCta.click();

    // Verify modal transitions without jarring visual flicker
    const bookingModal = page.locator('#f2f-scheduling-drawer');
    await expect(bookingModal).toHaveClass(/transition-smooth/);
    await expect(bookingModal).toBeVisible();

    // Populate session parameters derived from Company Document booking rules
    await page.selectOption('[data-testid="service-type"]', 'onsite-consultation');
    await page.fill('[data-testid="location-input"]', 'Athens Innovation Hub');
    await page.click('[data-testid="slot-available-first"]');

    // Complete checkout flow & verify feedback delight state
    await page.click('[data-testid="confirm-f2f-booking"]');
    const confirmationToast = page.locator('.toast-success');
    await expect(confirmationToast).toContainText('Your face-to-face consultation is confirmed');
  });

  test('REQ-REG-02: Micro-interaction elegance and error prevention in tenant settings', async ({ page }) => {
    await page.goto('/settings/hybrid-services');
    const toggle = page.locator('[data-testid="toggle-f2f-sync"]');
    await toggle.click();
    
    // Confirm inline validation adheres to Company Document SLA thresholds (<200ms response)
    const statusBadge = page.locator('[data-testid="sync-status"]');
    await expect(statusBadge).toHaveText('Active Synchronized', { timeout: 200 });
  });
});
```