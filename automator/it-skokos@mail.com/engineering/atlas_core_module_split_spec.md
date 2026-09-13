# Atlas Core Monolith Decoupling: Module Extraction Specification
**Author:** Zed Adeyemi  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D15 07:20  
**Inputs used:** Business Document (Company Document)  
## Summary

Architecture refactor document and boundary isolation plan detailing the extraction of core legacy modules into decoupled services, incorporating edge-case validation derived from Business Document: Company Document.

## Deliverable
```
# Architecture Refactoring Spec: Atlas Core Monolith Split
Author: Zed Adeyemi
Project: Atlas Core

## 1. Context & Business Grounding
Per 'Business Document: Company Document', the Atlas Core platform must separate real-time SaaS scheduling paths from offline Face to Face Service reconciliation without violating transactional consistency boundaries.

## 2. Decoupling Blueprint
- **Target Monolith Segment**: `com.itskokos.atlas.legacy.monolith`
- **Extracted Modules**:
  1. `atlas-saas-engine`: API-driven tenant orchestration.
  2. `atlas-f2f-service`: Face-to-face physical workflow sync.
  3. `atlas-shared-kernel`: Immutable event schemas and boundary interfaces.

## 3. Edge-Case Mitigation
- **Partial Disconnection during F2F Checkout**: Implemented outbox pattern with deterministic idempotency keys.
- **Cross-Domain Circular Dependencies**: Eliminated bi-directional entity mapping via event-driven pub/sub (Kafka/RabbitMQ).
- **Dual-Write Hazard**: Replaced legacy distributed locks with saga orchestration anchored by tenant lease tokens defined in 'Business Document: Company Document'.

## 4. Migration Plan & Backward Compatibility
1. Introduce anti-corruption layer (ACL) at `atlas-saas-engine` boundary.
2. Dual-route ingress traffic using dynamic feature flags.
3. Validate shadow reads against legacy monolith outputs before full traffic cutover.
```