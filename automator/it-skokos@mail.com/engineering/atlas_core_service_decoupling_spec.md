# Atlas Core Modularization: Domain-Driven Architecture & API Gateway Integration Spec
**Author:** Nova Ito  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D11 11:35  
**Inputs used:** Business Document (Company Document)  
## Summary

Architectural decoupling specification and service boundaries for decomposing the Atlas Core monolithic engine into dedicated microservices, ensuring seamless end-user interactions as outlined in Company Document.

## Deliverable
```
# Architectural Specification: Atlas Core Monolith Decomposition

## 1. Intent & UX Philosophy
Every millisecond of latency saved is a moment of calm restored for our users. By splitting the legacy monolith, Atlas Core evolves from an opaque engine into an orchestrated symphony of responsive services. Guided by the strategic objectives in **Company Document**, this refactor safeguards fluid UI transitions across both our SaaS platform and face-to-face operational touchpoints.

## 2. Service Boundary Map

### 2.1 Identity & Access (`atlas-auth-svc`)
- Extracted OAuth2/SAML flows and session state stores.
- Eliminates session locking bottlenecks during high-concurrency check-ins.

### 2.2 Client Experience Engine (`atlas-experience-svc`)
- Orchestrates bespoke SaaS dashboards and real-time face-to-face client booking workflows.
- Integrates event-driven updates via Redis Streams to eliminate jarring page reloads.

### 2.3 Core Billing & Ledger (`atlas-ledger-svc`)
- Isolated asynchronous transactional boundary adhering strictly to the compliance frameworks detailed in **Company Document**.

## 3. Integration & Routing Pattern
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: atlas-core-gateway
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  rules:
  - host: core.itskokos.internal
    http:
      paths:
      - path: /api/v2/experience
        pathType: Prefix
        backend:
          service:
            name: atlas-experience-svc
            port:
              number: 8080
      - path: /api/v2/auth
        pathType: Prefix
        backend:
          service:
            name: atlas-auth-svc
            port:
              number: 8081
```

## 4. Migration & Rollout Strategy
- Strangler Fig routing configured at the ingress layer.
- Canary deployment starting with internal staff accounts (10% traffic slice).
- Zero downtime fallback pipeline to ensure human-centered reliability.
```