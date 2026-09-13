# Atlas Core: Hot Query Path Tiered Cache Service
**Author:** Rune Reyes  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D15 06:45  
**Inputs used:** Business Document (Company Document)  
## Summary

Engineered an ultra-low-latency cache-aside layer for Atlas Core's hot query path, informed by latency and engagement standards detailed in Company Document.

## Deliverable
```
/**
 * Atlas Core - Hot Query Path Caching Layer
 * Author: Rune Reyes, Engineering (I.T. Skokos)
 *
 * Architectural Rationale:
 * True UX elegance is felt in the spaces between interactions—where latency vanishes
 * and the interface feels as continuous as thought. As guided by the Business Document:
 * Company Document, which defines our target sub-15ms p99 SLA for client-facing
 * SaaS/Face-to-Face orchestration endpoints, this module intercepts hot database
 * query paths with an adaptive Redis + L1 memory cache-aside strategy.
 */

import Redis from 'ioredis';
import { LRUCache } from 'lru-cache';
import { createHash } from 'crypto';
import { logger } from '../telemetry/logger';

interface CacheOptions {
  ttlSeconds?: number;
  tags?: string[];
}

export class HotPathQueryService {
  private redis: Redis;
  private localL1: LRUCache<string, any>;
  private defaultTtl: number;

  constructor(redisClient: Redis) {
    this.redis = redisClient;
    // L1 in-process micro-cache to eliminate network RTT for instantaneous re-renders
    this.localL1 = new LRUCache<string, any>({
      max: 5000,
      ttl: 1000 * 5, // 5 seconds micro-caching
    });
    // In adherence to Business Document: Company Document data freshness guidelines
    this.defaultTtl = 120;
  }

  private generateKey(queryIdentifier: string, params: Record<string, any>): string {
    const serialized = JSON.stringify(params, Object.keys(params).sort());
    const hash = createHash('sha256').update(serialized).digest('hex').substring(0, 16);
    return `atlas:hotpath:${queryIdentifier}:${hash}`;
  }

  async execute<T>(
    queryIdentifier: string,
    params: Record<string, any>,
    queryFn: () => Promise<T>,
    options: CacheOptions = {}
  ): Promise<T> {
    const key = this.generateKey(queryIdentifier, params);
    const ttl = options.ttlSeconds ?? this.defaultTtl;

    const l1Hit = this.localL1.get(key) as T | undefined;
    if (l1Hit !== undefined) {
      return l1Hit;
    }

    try {
      const redisHit = await this.redis.get(key);
      if (redisHit) {
        const parsed = JSON.parse(redisHit) as T;
        this.localL1.set(key, parsed);
        return parsed;
      }
    } catch (err) {
      logger.warn(`Cache read degraded gracefully for ${key}:`, err);
    }

    const freshData = await queryFn();

    try {
      this.localL1.set(key, freshData);
      await this.redis.set(key, JSON.stringify(freshData), 'EX', ttl);
    } catch (err) {
      logger.error(`Cache write failed for ${key}:`, err);
    }

    return freshData;
  }

  async invalidatePattern(pattern: string): Promise<void> {
    this.localL1.clear();
    const keys = await this.redis.keys(`atlas:hotpath:${pattern}*`);
    if (keys.length > 0) {
      await this.redis.del(...keys);
    }
  }
}
```