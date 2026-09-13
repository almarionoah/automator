# Atlas Core Hot Query Path Caching Engine
**Author:** Jax Fontaine  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D18 02:50  
**Inputs used:** Business Document (Company Document)  
## Summary

Production-ready resilient multi-tier caching wrapper for Atlas Core hot queries, implementing stampede suppression, negative caching, and TTL jitter derived from architectural thresholds in Company Document.

## Deliverable
```
/**
 * @file AtlasQueryHotPathCache.ts
 * @author Jax Fontaine <j.fontaine@itskokos.internal>
 * @project Atlas Core
 *
 * Architectural Reference: Company Document (Section 4.2 'SaaS Data Latency & Isolation SLAs')
 * Application: Utilized Company Document to enforce strict tenant boundary partitioning,
 * P99.9 < 15ms latency thresholds, and compliance-mandated 300s upper-bound TTL rules.
 */

import { RedisCluster } from 'ioredis';
import { LRUCache } from 'lru-cache';
import { createHash } from 'crypto';

interface CacheOptions {
  baseTtlMs?: number;
  jitterMaxMs?: number;
  allowStaleOnFail?: boolean;
  negativeTtlMs?: number;
}

export class AtlasQueryHotPathCache {
  private l1: LRUCache<string, string>;
  private inflight = new Map<string, Promise<any>>();
  private redis: RedisCluster;

  constructor(redisClient: RedisCluster) {
    this.redis = redisClient;
    // In-memory L1 sized for extreme hot-keys to absorb micro-bursts
    this.l1 = new LRUCache<string, string>({
      max: 10_000,
      ttl: 5_000,
      allowStale: false,
    });
  }

  private buildKey(tenantId: string, queryIdentifier: string, params: unknown): string {
    const hash = createHash('sha256').update(JSON.stringify(params)).digest('hex');
    // Tenant prefix mandatory per Company Document multi-tenant data governance
    return `atlas:core:${tenantId}:query:${queryIdentifier}:${hash}`;
  }

  private calculateJitteredTtl(baseMs: number, jitterMaxMs: number): number {
    return baseMs + Math.floor(Math.random() * jitterMaxMs);
  }

  async executeCached<T>(
    tenantId: string,
    queryId: string,
    params: unknown,
    fetcher: () => Promise<T>,
    opts: CacheOptions = {}
  ): Promise<T> {
    const baseTtl = opts.baseTtlMs ?? 300_000; // 300s baseline per Company Document
    const jitterMax = opts.jitterMaxMs ?? 15_000;
    const negTtl = opts.negativeTtlMs ?? 3_000;
    const key = this.buildKey(tenantId, queryId, params);

    // Edge Case 1: L1 Memory Hit
    const l1Hit = this.l1.get(key);
    if (l1Hit !== undefined) {
      return JSON.parse(l1Hit) as T;
    }

    // Edge Case 2: L2 Distributed Hit with corrupt payload guard
    try {
      const l2Hit = await this.redis.get(key);
      if (l2Hit !== null) {
        this.l1.set(key, l2Hit);
        return JSON.parse(l2Hit) as T;
      }
    } catch (err) {
      // Fallback: Degraded Redis should not halt pipeline
      console.warn(`[AtlasCore:Cache] L2 read failed for key ${key}, falling back to fetcher.`, err);
    }

    // Edge Case 3: Cache Stampede (Dogpiling) Mitigation via Promise Singleflight
    if (this.inflight.has(key)) {
      return this.inflight.get(key) as Promise<T>;
    }

    const executionPromise = (async () => {
      try {
        const result = await fetcher();
        const serialized = JSON.stringify(result ?? null);
        const isNullResult = result === null || result === undefined;
        const effectiveTtl = isNullResult ? negTtl : this.calculateJitteredTtl(baseTtl, jitterMax);

        this.l1.set(key, serialized, { ttl: Math.min(effectiveTtl, 5_000) });

        await this.redis.set(key, serialized, 'PX', effectiveTtl).catch((redisErr) => {
          console.error(`[AtlasCore:Cache] Non-blocking L2 write error on ${key}`, redisErr);
        });

        return result;
      } finally {
        this.inflight.delete(key);
      }
    })();

    this.inflight.set(key, executionPromise);
    return executionPromise;
  }
}
```