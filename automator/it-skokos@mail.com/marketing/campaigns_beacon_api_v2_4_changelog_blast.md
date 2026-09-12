# Beacon API v2.4 Changelog Blast Campaign Spec & Schedule
**Author:** Zed Hale  
**Department:** Marketing  
**Project:** Beacon API  
**Produced:** D3 04:45  
## Summary

Scheduled changelog broadcast package for Beacon API v2.4 covering email newsletter, community webhooks, and distribution schedule under stated release assumptions.

## Purchase

This package is sold through the company's live PayPal account.

- Price: USD 250.00
- Pay: https://www.paypal.com/checkoutnow?token=2AA57122U7122292X

## Deliverable
```
# CAMPAIGN SPEC: Beacon API v2.4 Changelog Blast

## 1. Assumptions
- Product: Beacon API (developer infra component of I.T. Skokos SaaS).
- Release Core: v2.4 introduced Ed25519 webhook signing, 40% p99 latency reduction via edge routing, and standardized rate-limiting headers (`X-Beacon-RateLimit-*`).
- Target Audience: Active developer accounts, API key holders, and technical integration leads (~14k recipients).
- Delivery Engine: Customer.io / SendGrid + Discord/Slack Developer Webhooks.
- Scheduled Time: Tuesday, 10:00 AM UTC (optimal developer engagement window).

---

## 2. Email Dispatch Config & Copy

- **Sender:** Zed Hale | I.T. Skokos Product Updates <changelog@itskokos.com>
- **Reply-To:** api-support@itskokos.com
- **Segment:** `api_users_active_30d` + `tier_enterprise_tech_leads`
- **UTM Tag:** `utm_source=changelog&utm_medium=email&utm_campaign=beacon_v2_4`
- **Subject Line:** [Changelog] Beacon API v2.4: 40% lower p99 latency + Ed25519 webhooks
- **Preheader:** Instant webhook verification, new rate-limit headers, and edge performance upgrades.

### Body Copy:
Hey {{ customer.first_name | default: "Developer" }},

Beacon API v2.4 is live with major upgrades to throughput, security, and developer ergonomics:

- ⚡ **40% Faster Edge Routing:** Global p99 latency dropped to 65ms across all read endpoints.
- 🔒 **Ed25519 Webhook Signing:** Cryptographically secure payload verification with zero replay vulnerability.
- 📊 **Granular Rate-Limit Headers:** Real-time quota visibility via `X-Beacon-RateLimit-Remaining` and `Reset` headers.
- 🛠️ **SDK Updates:** Python, Go, and Node SDKs updated with typed webhook parsers.

[Read Full Docs & Upgrade Guide ->](https://docs.itskokos.com/beacon/changelog/v2-4?utm_source=changelog&utm_medium=email)

---

## 3. Webhook Dispatch (Discord/Slack)
**Scheduled Trigger:** T-0 at email release
**Payload:**
🚀 **Beacon API v2.4 Released**
• 40% lower p99 edge latency
• Ed25519 Webhook signatures
• New rate-limit response headers
👉 Docs: https://docs.itskokos.com/beacon/changelog/v2-4
```