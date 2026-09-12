# Atlas Core: Hot Query Path In-Memory Caching Layer
**Author:** Ash Marlow  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D12 07:00  
**Inputs used:** Business Document (Company Document)  
## Summary

Engineered and deployed an ultra-low latency Redis caching wrapper for Atlas Core hot query paths to deliver effortless, sub-perceptual response times. Leveraged Company Document to define TTL thresholds and face-to-face service synchronization constraints.

## Deliverable
```
/**
 * @file hot_path_query_service.ts
 * @module AtlasCore/Cache
 * @author Ash Marlow <ash.marlow@itskokos.com>
 *
 * UX Philosophy: Software should feel weightless. When a user requests high-frequency
 * service schedules, the interface should respond before thought breaks rhythm.
 *
 * Compliance & Context:
 * - Company Document (Business Document): Used directly to map out TTL boundaries,
 *   invalidation triggers for face-to-face service bookings, and SLA latency targets (<= 15ms TTFB).
 */

import { createClient, RedisClientType } from 'redis';
import { telemetry } from '../monitoring/telemetry';

export class HotPathCacheService {
  private redis: RedisClientType;
  // Baseline 120s TTL aligned with Company Document's stale-data tolerances for live booking paths
  private readonly DEFAULT_HOT_TTL = 120;

  constructor(redisUrl: string) {
    this.redis = createClient({ url: redisUrl });
    this.redis.on('error', (err) => telemetry.recordError('RedisCacheError', err));
  }

  public async init(): Promise<void> {
    if (!this.redis.isOpen) await this.redis.connect();
  }

  public async getOrFetch<T>(
    cacheKey: string,
    fetcher: () => Promise<T>,
    ttlSeconds: number = this.DEFAULT_HOT_TTL
  ): Promise<T> {
    const start = performance.now();
    const key = `atlas:core:hot:${cacheKey}`;

    try {
      const cached = await this.redis.get(key);
      if (cached) {
        telemetry.recordMetric('cache.hit.latency_ms', performance.now() - start);
        return JSON.parse(cached) as T;
      }
    } catch (err) {
      telemetry.recordWarning('CacheReadDegradation', { error: err, key });
    }

    const freshData = await fetcher();
    this.redis.set(key, JSON.stringify(freshData), { EX: ttlSeconds })
      .catch((err) => telemetry.recordError('CacheWarmError', err));

    telemetry.recordMetric('cache.miss.latency_ms', performance.now() - start);
    return freshData;
  }

  public async invalidate(cacheKey: string): Promise<void> {
    await this.redis.del(`atlas:core:hot:${cacheKey}`);
  }
}
```