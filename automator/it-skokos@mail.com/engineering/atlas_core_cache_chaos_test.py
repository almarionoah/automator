# Chaos Engineering Test Plan & Implementation: Hot Query Path Caching Resilience
**Author:** Volt Okafor  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D11 07:05  
**Inputs used:** Business Document (Company Document)  
## Summary

Resilience and failure-injection test suite for the newly implemented Redis query cache on project Atlas Core, validated against baseline SLA targets specified in Company Document.

## Deliverable
```
"""
Atlas Core - Chaos Test Suite: Hot Query Path Cache Resilience
Author: Volt Okafor (Engineering / Chaos Testing)
Reference: Business Document: Company Document (SLA & Target Specifications)

Description:
Validates system degradation, cache penetration, and stampede mitigation
when the Atlas Core hot query path cache layer experiences intermittent latency,
eviction spikes, and complete node failure.
"""

import time
import pytest
import redis
from atlas_core.services import query_service
from atlas_core.chaos import inject_network_latency, drop_redis_connections

# Baseline SLA verified from Company Document: p99 < 45ms under cache hit, graceful degradation under miss.
COMPANY_DOC_SLA_P99_MS = 45

class TestHotQueryCacheChaos:
    @pytest.fixture(autouse=True)
    def setup_chaos(self):
        self.cache_client = redis.Redis(host='localhost', port=6379, db=0)
        yield
        self.cache_client.flushdb()

    def test_cache_stampede_under_sudden_eviction(self):
        # Simulate 500 concurrent threads hitting hot key during eviction
        key = "hot_path:tenant_summary:global"
        query_service.prime_cache(key)
        
        # Drop key and simulate instant burst
        self.cache_client.delete(key)
        results = query_service.concurrent_fetch(key, concurrency=500)
        
        assert results.single_flight_mutex_engaged is True
        assert results.database_queries_executed == 1
        assert results.max_latency_ms < COMPANY_DOC_SLA_P99_MS * 3

    def test_cache_node_partition_fallback(self):
        # Inject 100% packet loss to cache layer
        with drop_redis_connections():
            response = query_service.fetch_tenant_summary("tenant_1029")
            assert response.status == "SUCCESS"
            assert response.source == "POSTGRES_REPLICA_FALLBACK"

```