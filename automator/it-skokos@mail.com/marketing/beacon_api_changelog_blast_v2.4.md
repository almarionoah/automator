# Beacon API Changelog Dispatch Schedule & Campaign Copy
**Author:** Mint Reyes  
**Department:** Marketing  
**Project:** Beacon API  
**Produced:** D18 00:55  
**Inputs used:** Business Document (Company Document)  
## Summary

Cost-optimized changelog email blast configuration and lean markdown copy for Beacon API v2.4, referencing communication guidelines from the Company Document.

## Deliverable
```
# Campaign Dispatch & Changelog Blast: Beacon API v2.4
**Author:** Mint Reyes (Marketing)
**Target Audience:** Active Beacon API Developers & Enterprise SaaS Admins
**Execution Strategy:** Low-cost, plain-text/lean HTML hybrid utilizing existing transactional mail infrastructure to eliminate third-party ESP surcharge.

---

### Resource Utilization
- **Company Document**: Consulted the official *Company Document* to align messaging with I.T. Skokos branding, tone-of-voice rules, and compliance standards, avoiding the need for external agency review and reducing overhead.

---

### Dispatch Schedule Configuration
- **Trigger Window:** Tuesday, 10:00 AM UTC (Optimized for peak open rates without priority surcharge rates)
- **Audience Filter:** `users.beacon_api_active == true` (Filtered cohort to prevent sending to dormant seats, saving send tier quotas)
- **Cost Tier:** $0.00 (Routed via internal batch worker)

---

### Email Campaign Copy

**Subject:** [Changelog] Beacon API v2.4: Lower Latency & Face-to-Face Integration
**Preview:** See what's new in Beacon API v2.4—faster webhook processing, expanded hybrid service hooks, and optimized payload sizes.

Hi {{first_name | default: 'Developer'}},

We have deployed updates to the Beacon API to boost your platform performance and simplify hybrid face-to-face service orchestration.

**What’s New in Beacon API v2.4:**
1. **Lightweight Webhook Payloads:** Reduced default JSON payload size by 40%, saving bandwidth on high-throughput consumers.
2. **Hybrid Scheduling Endpoints:** Direct syncing between your SaaS workflows and I.T. Skokos Face to Face field agents.
3. **Rate Limit Resilience:** Improved burst handling for enterprise tier subscribers.

Review the full documentation and endpoint specs in our portal: https://developer.itskokos.com/beacon-api/v2.4

Best regards,
Mint Reyes | Marketing
I.T. Skokos
```