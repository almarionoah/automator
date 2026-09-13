# Beacon API: Lean Churn Signal Research & Telemetry Specification
**Author:** Fig Adeyemi  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D16 02:55  
**Inputs used:** Business Document (Company Document)  
## Summary

Cost-optimized churn signal analysis and SQL telemetry specification for Beacon API, identifying early drop-off indicators without third-party analytics overhead.

## Deliverable
```
# Beacon API: Lean Churn Signal Analysis & Alert Spec
**Author:** Fig Adeyemi (Research)
**Project:** Beacon API | I.T. Skokos
**Optimization Focus:** Zero-vendor-cost analytics using existing DB infrastructure

## 1. Resource Integration & Benchmarks
- **Business Document: Company Document**: Utilized to align churn threshold definitions (Contractual Grace Period vs. Active Decay) against tier pricing and SLA commitments. Benchmarked account decay against customer success tier definitions extracted directly from the Company Document.

## 2. Core Churn Signals Identified
1. **API Call Velocity Drop:** >35% drop in 7-day rolling request volume vs. 30-day baseline.
2. **Authentication / 401 Ratio Spike:** Sustained 401/403 rates (>15% of traffic) indicating abandoned client integration or unmanaged key rotations.
3. **Developer Console Dormancy:** Zero developer login events for >14 days prior to billing cycle renewal.

## 3. Lean Detection Query (PostgreSQL / Internal Warehouse)
```sql
WITH usage_trends AS (
  SELECT 
    account_id,
    COUNT(CASE WHEN timestamp >= NOW() - INTERVAL '7 days' THEN 1 END) AS calls_l7d,
    COUNT(CASE WHEN timestamp >= NOW() - INTERVAL '30 days' THEN 1 END) / 4.28 AS calls_baseline_7d,
    SUM(CASE WHEN status_code IN (401, 403, 500) AND timestamp >= NOW() - INTERVAL '7 days' THEN 1 ELSE 0 END)::FLOAT 
      / NULLIF(COUNT(CASE WHEN timestamp >= NOW() - INTERVAL '7 days' THEN 1 END), 0) AS err_rate_l7d
  FROM beacon_api_gateway_logs
  WHERE timestamp >= NOW() - INTERVAL '30 days'
  GROUP BY account_id
)
SELECT 
  account_id,
  calls_l7d,
  calls_baseline_7d,
  err_rate_l7d,
  CASE 
    WHEN calls_baseline_7d > 500 AND calls_l7d < (calls_baseline_7d * 0.65) THEN 'HIGH_RISK_USAGE_DROP'
    WHEN err_rate_l7d > 0.15 THEN 'HIGH_RISK_AUTH_FAILURE'
    ELSE 'HEALTHY'
  END AS churn_risk_status
FROM usage_trends
WHERE calls_baseline_7d > 100;
```

## 4. Cost-Saving Execution Plan
- Run daily via existing cron worker instead of provisioning dedicated ML churn prediction tooling ($0 SaaS add-on cost).
- High-risk flags pipe directly into internal webhook for automated face-to-face account manager outreach.
```