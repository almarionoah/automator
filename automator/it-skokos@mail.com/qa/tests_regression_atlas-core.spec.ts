# Atlas Core - Expanded Automated Regression Suite
**Author:** Echo Nkosi  
**Department:** QA  
**Project:** Atlas Core  
**Produced:** D12 09:35  
**Inputs used:** Business Document (Company Document)  
## Summary

Expanded the core regression test suite for Project Atlas Core to validate end-to-end SaaS workflows and Face-to-Face service booking pipelines, aligning coverage with the specifications defined in Business Document: Company Document.

## Deliverable
```
import { test, expect } from '@playwright/test';

/**
 * Project: Atlas Core
 * Author: Echo Nkosi (QA Agent)
 * Context & Alignment: Business Document: Company Document
 * Usage: Used 'Business Document: Company Document' to extract core user journeys, 
 * SLA compliance targets, and operational boundary conditions across SaaS and 
 * Face-to-Face hybrid service delivery.
 */

test.describe('Atlas Core - Expanded Regression Suite', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/login');
    await page.fill('#username', process.env.QA_TEST_USER || 'qa_user');
    await page.fill('#password', process.env.QA_TEST_PASS || 'qa_pass');
    await page.click('button[type="submit"]');
    await expect(page).toHaveURL(/.*dashboard/);
  });

  test('REQ-001: SaaS Tenant Workflow Provisioning', async ({ page }) => {
    // Validating tenant provisioning flow derived from Company Document Section 2.1
    await page.click('nav >> text=Tenants');
    await page.click('#btn-create-tenant');
    await page.fill('#tenant-name', 'Regression Tenant Auto');
    await page.selectOption('#tier-select', 'ENTERPRISE');
    await page.click('#submit-provisioning');
    
    const toast = page.locator('.notification-success');
    await expect(toast).toBeVisible();
    await expect(toast).toContainText('Tenant provisioned successfully');
  });

  test('REQ-002: Face-to-Face Service Scheduling & Dispatch', async ({ page }) => {
    // Validating on-site appointment booking per Company Document Section 3.4
    await page.click('nav >> text=Field Services');
    await page.click('#book-f2f-session');
    await page.fill('#client-id', 'CL-9942');
    await page.fill('#service-location', 'HQ Onsite - Room 4B');
    await page.fill('#date-picker', '2025-06-15T10:00');
    await page.click('#confirm-dispatch');

    const statusBadge = page.locator('#booking-status');
    await expect(statusBadge).toHaveText('CONFIRMED_DISPATCHED');
  });
});
```