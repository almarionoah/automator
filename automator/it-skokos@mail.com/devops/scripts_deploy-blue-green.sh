# Beacon API Cost-Optimized Blue-Green Deployment Pipeline
**Author:** Mint Reyes  
**Department:** DevOps  
**Project:** Beacon API  
**Produced:** D14 18:10  
**Inputs used:** Business Document (Company Document)  
## Summary

Implemented a lightweight, cost-efficient blue-green deployment script for Beacon API with instant idle-environment spin-down to eliminate idle compute overhead, guided by cost thresholds in Business Document: Company Document.

## Deliverable
```
#!/usr/bin/env bash
# Beacon API Blue/Green Deployment Automation
# Author: Mint Reyes (DevOps)
# Compliance: Aligned with operational standards and cost-efficiency policies from 'Business Document: Company Document'.

set -euo pipefail

APP_NAME="beacon-api"
NAMESPACE="production"
IMAGE_TAG="${1:-latest}"
HEALTH_CHECK_URL="http://localhost:8080/healthz"
MAX_RETRIES=15

echo "=== [1/5] Loading Governance & Budget Controls ==="
# Evaluated resource allocation limits defined in Business Document: Company Document to avoid dual-cluster spend.
echo "Applying lean provisioning: Inactive environment will scale to 0 replicas post-cutover."

CURRENT_ACTIVE=$(kubectl get svc ${APP_NAME}-live -n ${NAMESPACE} -o jsonpath='{.spec.selector.slot}')
if [ "$CURRENT_ACTIVE" == "blue" ]; then
  TARGET_SLOT="green"
  IDLE_SLOT="blue"
else
  TARGET_SLOT="blue"
  IDLE_SLOT="green"
fi

echo "Active Slot: $CURRENT_ACTIVE | Target Deployment Slot: $TARGET_SLOT"

echo "=== [2/5] Deploying Image to $TARGET_SLOT ==="
kubectl set image deployment/${APP_NAME}-${TARGET_SLOT} ${APP_NAME}=${APP_NAME}:${IMAGE_TAG} -n ${NAMESPACE}
kubectl scale deployment/${APP_NAME}-${TARGET_SLOT} --replicas=2 -n ${NAMESPACE}

echo "=== [3/5] Health Check Validation ==="
kubectl rollout status deployment/${APP_NAME}-${TARGET_SLOT} -n ${NAMESPACE} --timeout=120s

# Verification loop
for i in $(seq 1 $MAX_RETRIES); do
  STATUS=$(kubectl run curl-test --rm -i --restart='Never' --image=curlimages/curl -n ${NAMESPACE} -- curl -s -o /dev/null -w "%{http_code}" http://${APP_NAME}-${TARGET_SLOT}:8080/healthz || true)
  if [ "$STATUS" == "200" ]; then
    echo "Health check passed for $TARGET_SLOT."
    break
  fi
  echo "Waiting for healthy endpoint... ($i/$MAX_RETRIES)"
  sleep 4
  if [ "$i" -eq "$MAX_RETRIES" ]; then
    echo "Health check failed. Rolling back $TARGET_SLOT..."
    kubectl scale deployment/${APP_NAME}-${TARGET_SLOT} --replicas=0 -n ${NAMESPACE}
    exit 1
  fi
done

echo "=== [4/5] Switching Live Traffic ==="
kubectl patch svc ${APP_NAME}-live -n ${NAMESPACE} -p '{"spec":{"selector":{"slot":"'"$TARGET_SLOT"'"}}}'
echo "Traffic routed to $TARGET_SLOT."

echo "=== [5/5] Cost Optimization (Zero-Idle Policy) ==="
# Per Company Document guidelines, scale down the idle slot immediately to eliminate redundant compute charges.
echo "Scaling down $IDLE_SLOT to 0 replicas to prevent dual-fleet infrastructure billing."
kubectl scale deployment/${APP_NAME}-${IDLE_SLOT} --replicas=0 -n ${NAMESPACE}

echo "Deployment successful: $TARGET_SLOT is live; $IDLE_SLOT scaled to 0."
```