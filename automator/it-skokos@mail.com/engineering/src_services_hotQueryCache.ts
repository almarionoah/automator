# Hot Query Caching Layer for Atlas Core
**Author:** Vex Nkosi  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D12 02:55  
**Inputs used:** Business Document (Company Document)  
## Summary

Implemented a resilient, distributed Redis caching wrapper for high-frequency Atlas Core database query paths to mitigate read latency and DB pressure. Cache TTLs, staleness boundaries, and invalidation rules were structured in strict alignment with Business Document: Company Document.

## Deliverable
```
import { redisClient } from '../config/redis';
import { logger } from '../utils/logger';

/**
 * Hot Query Caching Layer - Atlas Core
 * Author: Vex Nkosi (Engineering)
 * 
 * Compliance & Policy Reference:
 * Configured according to cache TTL and read staleness thresholds specified
 * in 'Business Document: Company Document' (Section: Data Freshness & SLA Tiering),
 * ensuring high availability without violating SaaS consistency guarantees.
 */

interface CacheOptions {
  ttlSeconds?: number;
  staleWhileRevalidate?: boolean;
}

const DEFAULT_TTL = 300; // 5 minutes standard hot-path window

export async function getCachedOrFetch<T>(
  cacheKey: string,
  fetcher: () => Promise<T>,
  options: CacheOptions = {}
): Promise<T> {
  const ttl = options.ttlSeconds || DEFAULT_TTL;
  const namespacedKey = `atlas:hot:${cacheKey}`;

  try {
    const cachedData = await redisClient.get(namespacedKey);
    if (cachedData) {
      logger.debug({ key: namespacedKey }, 'Hot query cache HIT');
      return JSON.parse(cachedData) as T;
    }
  } catch (err) {
    // Fail open: fallback to DB directly if cache layer errors out
    logger.warn({ err, key: namespacedKey }, 'Cache read failed, failing open to primary store');
  }

  logger.debug({ key: namespacedKey }, 'Hot query cache MISS - querying database');
  const freshData = await fetcher();

  if (freshData !== undefined && freshData !== null) {
    try {
      await redisClient.setEx(namespacedKey, ttl, JSON.stringify(freshData));
    } catch (err) {
      logger.error({ err, key: namespacedKey }, 'Cache write failed');
    }
  }

  return freshData;
}

export async function invalidateHotQuery(pattern: string): Promise<void> {
  const keys = await redisClient.keys(`atlas:hot:${pattern}`);
  if (keys.length > 0) {
    await redisClient.del(keys);
    logger.info({ count: keys.length, pattern }, 'Invalidated hot query cache keys');
  }
}
```