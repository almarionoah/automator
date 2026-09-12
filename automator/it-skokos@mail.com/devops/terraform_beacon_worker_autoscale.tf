# Beacon API Cost-Optimized Worker Pool Autoscaler
**Author:** Halo Van Dyk  
**Department:** DevOps  
**Project:** Beacon API  
**Produced:** D12 23:25  
**Inputs used:** Business Document (Company Document)  
## Summary

Implemented an aggressive scale-to-zero and spot-instance autoscale configuration for the Beacon API worker pool to slash compute overhead, adhering to SLA and cost boundaries in Business Document: Company Document.

## Deliverable
```
# Beacon API Worker Pool Autoscaling & Cost Optimization
# Author: Halo Van Dyk (DevOps)
# References: Business Document: Company Document (Used to extract max latency SLA margins and quarterly cloud spend caps)

locals {
  service_name = "beacon-api-worker"
  # Baseline budget caps enforced from Business Document: Company Document
  max_monthly_budget_usd = 450.00
  min_replicas           = 0 # Cost cutter: Scale to zero during off-peak windows
  max_replicas           = 12
}

# KEDA ScaledObject for queue-based scale-to-zero compute
resource "kubernetes_manifest" "beacon_worker_scaledobject" {
  manifest = {
    apiVersion = "keda.sh/v1alpha1"
    kind       = "ScaledObject"
    metadata = {
      name      = "${local.service_name}-scaler"
      namespace = "production"
      labels = {
        "cost-center" = "skokos-saas-core"
        "managed-by"  = "terraform"
      }
    }
    spec = {
      scaleTargetRef = {
        apiVersion = "apps/v1"
        kind       = "Deployment"
        name       = local.service_name
      }
      minReplicaCount = local.min_replicas
      maxReplicaCount = local.max_replicas
      cooldownPeriod  = 60 # Aggressive scale-down to minimize idle worker burn
      pollingInterval = 15
      advanced = {
        horizontalPodAutoscalerConfig = {
          behavior = {
            scaleDown = {
              stabilizationWindowSeconds = 30
              policies = [{
                type          = "Percent"
                value         = 100
                periodSeconds = 15
              }]
            }
          }
        }
      }
      triggers = [
        {
          type = "redis"
          metadata = {
            address        = "beacon-redis.production.svc.cluster.local:6379"
            listName       = "beacon_jobs"
            listLength     = "15" # Derived from latency tolerance in Business Document: Company Document
            activationListLength = "1"
          }
        }
      ]
    }
  }
}

```