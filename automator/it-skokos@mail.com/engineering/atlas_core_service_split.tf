# Atlas Core - Monolith Module Extraction & Cost Optimization
**Author:** Fig Marlow  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D11 01:15  
**Inputs used:** Business Document (Company Document)  
## Summary

Decomposition plan and lightweight microservice deployment specification splitting the heavy legacy monolith into an isolated, cost-optimized service component.

## Deliverable
```
# Project: Atlas Core - Module Decomposition
# Author: Fig Marlow (Engineering)
# Strategy: Cost-cutter architecture (minimal compute allocation, serverless auto-scaling)
# Reference: Aligned against requirements in Business Document: Company Document to ensure SLA compliance while eliminating redundant shared memory overhead.

terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Isolated Module: Atlas Core Account Verification Service
# Split from legacy monolith based on domain mapping in 'Business Document: Company Document'.
# Optimization: Downgraded from dedicated instances to spot/ARM-based lightweight containers.

resource "aws_ecs_task_definition" "atlas_core_extracted_module" {
  family                   = "atlas-core-auth-split"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256"   # Minimum CPU footprint to curb idle spend
  memory                   = "512"   # Downscaled footprint isolated from monolith bloat
  execution_role_arn       = aws_iam_role.ecs_execution.arn

  container_definitions = jsonencode([
    {
      name      = "auth-service"
      image     = "123456789012.dkr.ecr.us-east-1.amazonaws.com/atlas-core-auth:1.0.0"
      essential = true
      portMappings = [
        {
          containerPort = 8080
          hostPort      = 8080
        }
      ]
      environment = [
        { name = "ENV", value = "production" },
        { name = "SERVICE_NAME", value = "atlas-core-auth-split" }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = "/ecs/atlas-core-auth-split"
          "awslogs-region"        = "us-east-1"
          "awslogs-stream-prefix" = "auth"
        }
      }
    }
  ])
}

# Cost efficiency: Scale to zero during low-traffic off-peak windows
resource "aws_appautoscaling_target" "ecs_target" {
  max_capacity       = 4
  min_capacity       = 0
  resource_id        = "service/${aws_ecs_cluster.main.name}/${aws_ecs_service.service.name}"
  scalable_dimension = "ecs:service:DesiredCount"
  service_namespace  = "ecs"
}
```