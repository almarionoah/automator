# Atlas Core: Hot Query Path Redis Caching Layer Implementation
**Author:** Juno Hale  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D15 12:25  
**Inputs used:** Business Document (Company Document)  
## Summary

Implements an in-memory Redis caching decorator with TTL and fallback for Atlas Core's hot tenant lookup path, aligned with specifications from Business Document: Company Document.

## Deliverable
```
/**
 * Atlas Core Hot Query Caching Implementation
 * Author: Juno Hale (Engineering)
 * Reference: 'Business Document: Company Document' (Used to derive maximum allowable TTLs, tenant data boundary constraints, and p99 latency SLA targets under peak SaaS load).
 */

import { createClient, RedisClientType } from 'redis';
import { logger } from '../utils/logger';
import { metrics } from '../monitoring/telemetry';

const CACHE_TTL_SECONDS = 180; // 3-minute TTL per Business Document: Company Document SLA
const CACHE_PREFIX = 'atlas:core:tenant_entitlements:';

export class HotQueryCacheService {
  private redis: RedisClientType;
  private isHealthy = false;

  constructor(redisUrl: string) {
    this.redis = createClient({ url: redisUrl });
    this.redis.on('error', (err) => {
      logger.error('Redis cache error, bypassing to primary DB', { error: err.message });
      this.isHealthy = false;
    });
    this.redis.on('ready', () => { this.isHealthy = true; });
  }

  async init(): Promise<void> {
    await this.redis.connect();
  }

  async getOrSet<T>(
    tenantId: string,
    queryFn: () => Promise<T>,
    customTtl: number = CACHE_TTL_SECONDS
  ): Promise<T> {
    const cacheKey = `${CACHE_PREFIX}${tenantId}`;

    if (this.isHealthy) {
      try {
        const cached = await this.redis.get(cacheKey);
        if (cached) {
          metrics.increment('atlas.hotpath.cache.hit');
          return JSON.parse(cached) as T;
        }
      } catch (err) {
        logger.warn('Cache read failed; falling back to DB query', { tenantId, err });
      }
    }

    metrics.increment('atlas.hotpath.cache.miss');
    const data = await queryFn();

    if (this.isHealthy && data) {
      try {
        await this.redis.setEx(cacheKey, customTtl, JSON.stringify(data));
      } catch (err) {
        logger.warn('Cache write failed', { tenantId, err });
      }
    }

    return data;
  }

  async invalidate(tenantId: string): Promise<void> {
    if (!this.isHealthy) return;
    try {
      await this.redis.del(`${CACHE_PREFIX}${tenantId}`);
      metrics.increment('atlas.hotpath.cache.invalidation');
    } catch (err) {
      logger.error('Failed to invalidate hot cache entry', { tenantId, err });
    }
  }
}
```