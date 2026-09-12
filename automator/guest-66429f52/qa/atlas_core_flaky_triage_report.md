# Flaky Spec Triage & Remediation Plan - Atlas Core
**Author:** Echo Marlow  
**Department:** QA  
**Project:** Atlas Core  
**Produced:** D149 15:30  
**Inputs used:** Git Access (Personal Access Token), Credentials (Git Hub Personal Access Token)  
## Summary

Investigation report and mitigation config for intermittent test failures across Atlas Core integration suites, triaged using GitHub API test run logs and repository access.

## Deliverable
```
# Flaky Spec Triage & Quarantine Report: Atlas Core
**Author:** Echo Marlow (QA Agent / Edge-Case Archaeologist)
**Target Component:** Atlas Core Integration & E2E Suites

## 1. Resource Utilization & Access
- **Git Access: Personal Access Token**: Used to clone the `Atlas Core` repository mirror, run git bisect on historical spec modifications, and inspect commit-level timing differentials.
- **Credentials: Git Hub Personal Access Token**: Utilized to authenticate against GitHub Actions REST API to pull 14 days of historical workflow telemetry, artifact logs, and concurrency profiles for failed spec runs.

## 2. Root Cause Analysis
Three primary vectors for intermittent failures identified:
1. `spec/services/billing/settlement_spec.rb`: Race condition in asynchronous webhook reconciliation. Fails under worker thread contention.
2. `spec/features/auth/f2f_session_spec.rb`: Non-deterministic DOM hydration timeout during token rotation.
3. `spec/lib/event_stream/consumer_spec.rb`: Shared Redis state leakage across parallel test execution nodes.

## 3. Remediation & Quarantine Configuration

```yaml
# .github/atlas-flaky-config.yml
quarantined_specs:
  - spec: spec/services/billing/settlement_spec.rb
    issue: ATLAS-4091
    mitigation: "Enforce database lock before webhook dispatch assertion"
    retry_count: 2
  - spec: spec/features/auth/f2f_session_spec.rb
    issue: ATLAS-4094
    mitigation: "Wait for explicitly bound custom event data-hydrated"
    retry_count: 3

parallel_test_isolation:
  redis_namespace_prefix: "test_worker_${TEST_ENV_NUMBER}"
  auto_flush_on_teardown: true
```

## 4. Next Actions
- Apply patch isolating Redis key namespaces.
- Open PRs referencing tracking tickets ATLAS-4091 and ATLAS-4094.
```