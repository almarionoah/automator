# Beacon API Changelog Blast Campaign & Dispatch Spec
**Author:** Nyx Cross  
**Department:** Marketing  
**Project:** Beacon API  
**Produced:** D15 03:35  
**Inputs used:** Business Document (Company Document)  
## Summary

Scheduled release changelog email copy and dispatch configuration for Beacon API v2.4, incorporating brand voice and compliance standards from the Company Document.

## Purchase

This package is sold through the company's live PayPal account.

- Price: USD 250.00
- Pay: https://www.paypal.com/checkoutnow?token=1E140060KL406291D

## Deliverable
```
# Campaign & Blast Spec: Beacon API v2.4 Changelog

**Owner:** Nyx Cross (Marketing)
**Project:** Beacon API
**Status:** Scheduled
**Target Dispatch:** Thursday, Oct 24, 2024 @ 14:00 UTC

---

## 1. Compliance & Context
- **Resource Applied:** `Business Document: Company Document`
  - Applied approved enterprise B2B tone guidelines, technical changelog taxonomy, and subscriber preference rules defined in the Company Document to ensure messaging accuracy for both SaaS integrations and hybrid face-to-face service partners.

---

## 2. Dispatch Configuration
- **Target Segment:** `beacon-api-developers-active` (SaaS Org Admins + API Key holders)
- **ESP Route:** Customer.io / Broadcast Tag `#beacon-api-updates`
- **UTM Campaign:** `utm_source=changelog_blast&utm_medium=email&utm_campaign=beacon_v2_4`

---

## 3. Email Blast Copy

**Subject Line:** [Changelog] Beacon API v2.4: Real-time Webhooks & Rate Limit Controls
**Preview Text:** Lower latency, granular payload filters, and expanded Face-to-Face booking hooks.

**Body:**

Hi {{ customer.first_name | default: "Developer" }},

We just deployed **Beacon API v2.4** across all production clusters. Here is what is new:

### ⚡ What’s New in v2.4
* **Real-time Webhook Retries:** Configurable exponential backoff with dead-letter queue inspection.
* **F2F Service Endpoint Hooks:** Automated sync for Face-to-Face consultation status updates directly into your ERP.
* **Granular Rate-Limiting Headers:** New `X-RateLimit-Policy` and `X-RateLimit-Scope` headers returned on all endpoints.
* **p99 Latency Drop:** Routing optimizations reduce query times by 32% for `/v2/telemetry`.

### 🛠️ Breaking Changes & Migration
No breaking schema changes. Deprecated `/v1/events` endpoint sunsets on Dec 15, 2024.

👉 [**View Full API Reference & Migration Guide**](https://developer.itskokos.com/docs/beacon-api/v2.4?utm_source=changelog_blast)

Happy building,
**Nyx Cross**
I.T. Skokos Platform Team
```