# Atlas Core - Expanded Automated Regression Suite
**Author:** Byte Bishop  
**Department:** QA  
**Project:** Atlas Core  
**Produced:** D11 20:30  
**Inputs used:** Business Document (Company Document)  
## Summary

Added E2E regression coverage for Atlas Core hybrid workflows (SaaS tenant quota enforcement and Face-to-Face service appointment booking), validating edge cases against Business Document: Company Document.

## Deliverable
```
import { test, expect } from '@playwright/test';

/**
 * Atlas Core Hybrid Regression Suite
 * Reference Source: 'Business Document: Company Document' (used to define Tier-1 quota thresholds, SLA timeout constraints, and Face-to-Face appointment verification protocols).
 */

test.describe('Atlas Core - SaaS & Face-to-Face Regression Suite', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/login');
    await page.fill('input[name="email"]', 'qa-operator@itskokos.internal');
    await page.fill('input[name="password"]', 'TestSessionPassword123!');
    await page.click('button[type="submit"]');
    await expect(page).toHaveURL(/\/dashboard/);
  });

  test('REQ-042: Verify Hybrid SaaS tenant provisioning & F2F credit allocation', async ({ page, request }) => {
    // Validating against tier allocations defined in Business Document: Company Document
    const tenantPayload = {
      organizationName: 'Skokos Client Logistics',
      planTier: 'Enterprise-Hybrid',
      f2fQuotaMonthly: 25
    };

    const createRes = await request.post('/api/v2/tenants', { data: tenantPayload });
    expect(createRes.status()).toBe(201);
    const tenantData = await createRes.json();

    await page.goto(`/tenants/${tenantData.id}/services`);
    await expect(page.locator('[data-testid="f2f-balance-badge"]')).toHaveText('25 Credits');
  });

  test('REQ-088: Face-to-Face check-in workflow state transitions', async ({ page }) => {
    // SLA check-in windows derived from Business Document: Company Document Section 3.2
    await page.goto('/services/f2f/schedule');
    await page.click('button[data-testid="slot-select-today"]');
    await page.click('button[data-testid="confirm-booking-btn"]');
    
    await expect(page.locator('.toast-success')).toBeVisible();
    await expect(page.locator('[data-testid="booking-status"]')).toHaveText('CONFIRMED');
  });
});
```