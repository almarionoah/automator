# Beacon API Churn Signal Analysis and Low-Cost Detection Framework
**Author:** Rune Okafor  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D17 01:20  
**Inputs used:** Business Document (Company Document)  
## Summary

Cost-optimized research report and SQL-based detection framework identifying early churn signals for Beacon API customers without procuring external retention software.

## Deliverable
```
-- Research Artefact: Beacon API Churn Signal Framework
-- Author: Rune Okafor, Research (o3)
-- Approach: Cost-Cutter (Utilizing existing Postgres logs to avoid third-party analytics subscriptions)
-- Reference: 'Business Document: Company Document' (used to establish baseline revenue tiers, SLA thresholds, and historical contract renewal churn patterns).

/* 
RESEARCH SUMMARY & SIGNALS IDENTIFIED:
1. 30-day API call volume contraction > 35% relative to previous 60-day moving average.
2. Invalidation of 4xx rate anomalies (client-side unhandled errors indicating abandoned integration).
3. Zero dashboard logins coupled with webhook failure suppression.
*/

-- Signal 1 & 2 Query: Early Contraction and Unhandled Integration Errors (Runs on standard read-replica)
WITH usage_trends AS (
    SELECT 
        account_id,
        COUNT(CASE WHEN created_at >= NOW() - INTERVAL '30 days' THEN 1 END) AS recent_calls,
        COUNT(CASE WHEN created_at BETWEEN NOW() - INTERVAL '90 days' AND NOW() - INTERVAL '31 days' THEN 1 END) / 2.0 AS baseline_30d_avg,
        COUNT(CASE WHEN status_code >= 400 AND created_at >= NOW() - INTERVAL '30 days' THEN 1 END) * 1.0 / 
            NULLIF(COUNT(CASE WHEN created_at >= NOW() - INTERVAL '30 days' THEN 1 END), 0) AS recent_error_rate
    FROM beacon_api_request_logs
    WHERE created_at >= NOW() - INTERVAL '90 days'
    GROUP BY account_id
)
SELECT 
    u.account_id,
    u.recent_calls,
    u.baseline_30d_avg,
    ROUND(u.recent_error_rate, 4) AS error_rate,
    CASE 
        WHEN u.recent_calls = 0 THEN 'CRITICAL_ABANDONED'
        WHEN u.recent_calls < (u.baseline_30d_avg * 0.65) THEN 'HIGH_CONTRACTION'
        WHEN u.recent_error_rate > 0.15 THEN 'INTEGRATION_FATIGUE'
        ELSE 'HEALTHY'
    END AS churn_risk_status
FROM usage_trends u
WHERE u.recent_calls < (u.baseline_30d_avg * 0.65) OR u.recent_error_rate > 0.15;
```