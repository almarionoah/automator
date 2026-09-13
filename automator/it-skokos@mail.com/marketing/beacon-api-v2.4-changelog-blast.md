# Beacon API Changelog Blast Campaign & Distribution Schedule
**Author:** Halo Petrov  
**Department:** Marketing  
**Project:** Beacon API  
**Produced:** D15 07:00  
**Inputs used:** Business Document (Company Document)  
## Summary

Scheduled marketing changelog dispatch for Beacon API v2.4 with deep-linked documentation assets, utilizing Business Document: Company Document for brand messaging and audience tiering.

## Deliverable
```
# Campaign Dispatch Spec: Beacon API v2.4 Changelog Blast
**Owner:** Halo Petrov (Marketing / Docs Evangelist)
**Target Release Date:** October 24, 2024 | 14:00 UTC
**Channels:** Customer Email (Customer.io), In-App Announcement Modal, Developer Portal Banner

---

### Resource Utilization
- **Business Document: Company Document**: Utilized section 4.2 (External Comms Governance) to verify tier-specific dispatch thresholds for SaaS and Face to Face service clients, and aligned tone-of-voice constraints with brand documentation guidelines.

---

### Blast Email Draft

**Subject:** [Beacon API] v2.4 Released: Webhook idempotency, lower latency, and updated docs
**Preview Text:** Explore new rate-limiting headers, batch sync endpoints, and our updated migration guides.

**Body:**

Hey Developer,

We’ve just shipped **Beacon API v2.4**, focused on resilience, telemetry granularity, and streamlined integration across both our SaaS platform and Face to Face operational workflows.

#### What’s New:
- **Idempotency Keys on `/v2/events`**: Prevent duplicate telemetry submissions during network retries. Read the docs: `docs.itskokos.com/beacon/idempotency`
- **Batch Webhook Dispatch**: Aggregate up to 500 payload events per push. See specs: `docs.itskokos.com/beacon/webhooks#batch`
- **Live Latency Diagnostics**: Query edge node status directly via `/v2/health/edge`.

#### Documentation First:
Every update includes executable code samples, OpenAPI specs, and updated Postman collections in our central docs portal. Review the full release notes and updated schema:

👉 **[Read Full Changelog & API Reference (v2.4)](https://docs.itskokos.com/beacon/changelog/v2-4)**

---
*Need dedicated support? Reach out via portal ticket or schedule an on-site walkthrough with our Face to Face services team.*
```