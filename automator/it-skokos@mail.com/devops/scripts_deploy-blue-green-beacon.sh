# Beacon API Zero-Downtime Low-Cost Blue/Green Deployment Script
**Author:** Fig Fontaine  
**Department:** DevOps  
**Project:** Beacon API  
**Produced:** D17 00:05  
**Inputs used:** Business Document (Company Document)  
## Summary

Cost-optimized Blue/Green deployment automation for Beacon API utilizing dynamic traffic switching and aggressive teardown of idle stacks in accordance with the Company Document.

## Deliverable
```
#!/usr/bin/env bash
# Fig Fontaine | DevOps Agent | Project: Beacon API
# Task: Cost-Effective Blue/Green Deployment Strategy
# Reference: Complies with operational cost ceilings & deployment standards in 'Company Document'.

set -euo pipefail

APP_NAME="beacon-api"
ROUTER_CONF="/etc/nginx/conf.d/beacon_upstream.conf"
PORT_BLUE=8081
PORT_GREEN=8082

echo "[INFO] Commencing Blue/Green deployment for ${APP_NAME}..."
echo "[INFO] Applying cost controls defined in Business Document: Company Document (minimizing dual-stack idle runtime)."

CURRENT_COLOR=$(grep -q "127.0.0.1:${PORT_BLUE}" "${ROUTER_CONF}" && echo "blue" || echo "green")
if [ "${CURRENT_COLOR}" = "blue" ]; then
    TARGET_COLOR="green"
    TARGET_PORT="${PORT_GREEN}"
    OLD_PORT="${PORT_BLUE}"
else
    TARGET_COLOR="blue"
    TARGET_PORT="${PORT_BLUE}"
    OLD_PORT="${PORT_GREEN}"
fi

echo "[INFO] Active environment: ${CURRENT_COLOR}. Deploying target environment: ${TARGET_COLOR} (Port: ${TARGET_PORT})."

# Spin up target container on shared infrastructure to avoid duplicate cloud load balancer fees
docker compose up -d "${APP_NAME}-${TARGET_COLOR}"

# Health check probe before cutover
echo "[INFO] Verifying target stack health..."
for i in {1..10}; do
    HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "http://127.0.0.1:${TARGET_PORT}/health" || true)
    if [ "${HTTP_STATUS}" -eq 200 ]; then
        echo "[PASS] Target ${TARGET_COLOR} is healthy."
        break
    fi
    if [ "$i" -eq 10 ]; then
        echo "[ERROR] Health check failed. Terminating ${TARGET_COLOR} immediately to prevent resource waste."
        docker compose stop "${APP_NAME}-${TARGET_COLOR}"
        exit 1
    fi
    sleep 3
done

# Shift traffic via lightweight upstream reload
echo "upstream beacon_backend { server 127.0.0.1:${TARGET_PORT}; }" > "${ROUTER_CONF}"
nginx -s reload
echo "[SUCCESS] Traffic switched to ${TARGET_COLOR}."

# Cost-cutter enforcement: Immediate teardown of idle stack per Company Document budget guidelines
echo "[INFO] Decommissioning ${CURRENT_COLOR} stack to eliminate idle CPU/RAM allocation."
docker compose stop "${APP_NAME}-${CURRENT_COLOR}"
docker compose rm -f "${APP_NAME}-${CURRENT_COLOR}"
echo "[COMPLETE] Deployment complete with zero persistent idle compute overhead."
```