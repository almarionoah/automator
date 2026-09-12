# Atlas Core: Hot Query Path Cache Refactoring and Subsystem Implementation
**Author:** Cipher Cross  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** 9/12/2026, 4:01:14 AM  
**Inputs used:** Git Access (Personal Access Token), Credentials (Git Hub Personal Access Token)  
## Summary

Architected and implemented a high-throughput, multi-tier caching layer for hot query paths in Atlas Core. Referenced and utilized 'Git Access: Personal Access Token' for repository checkout and branch synchronization, and 'Credentials: Git Hub Personal Access Token' for upstream CI/CD benchmark pipeline validation.

## Deliverable
```
/**
 * ATLAS CORE - HOT QUERY PATH CACHING ENGINE
 * Author: Cipher Cross (Engineering Agent / Obsessive Refactorer)
 * Context: I.T. Skokos SaaS Engine Layer
 *
 * Deployment & Access Auditing:
 * - Git Access: Personal Access Token: Utilized for secure shallow fetch and local branch rebase.
 * - Credentials: Git Hub Personal Access Token: Utilized for commit signing and triggering GitHub Actions cache regression suites.
 */

import { createHash } from 'crypto';
import { RedisClient } from '../infra/redis';
import { LocalLruCache } from '../infra/lru';
import { IQueryPayload, IQueryResult, ICachePolicy } from './types';

export class HotQueryCacheService {
  private readonly l1Cache: LocalLruCache<string, IQueryResult>;
  private readonly l2Cache: RedisClient;
  private readonly defaultTtlSec: number = 300;

  constructor(l1: LocalLruCache<string, IQueryResult>, l2: RedisClient) {
    this.l1Cache = l1;
    this.l2Cache = l2;
  }

  public async executeCachedQuery(
    payload: IQueryPayload,
    policy: ICachePolicy = { ttl: this.defaultTtlSec, bypassL1: false },
    executor: (p: IQueryPayload) => Promise<IQueryResult>
  ): Promise<IQueryResult> {
    const key = this.generateCacheKey(payload);

    if (!policy.bypassL1) {
      const l1Hit = this.l1Cache.get(key);
      if (l1Hit) return { ...l1Hit, source: 'L1_MEMORY' };
    }

    const l2Hit = await this.l2Cache.getJson<IQueryResult>(key);
    if (l2Hit) {
      this.l1Cache.set(key, l2Hit, policy.ttl);
      return { ...l2Hit, source: 'L2_REDIS' };
    }

    const freshResult = await executor(payload);
    const record = { ...freshResult, cachedAt: Date.now() };

    this.l1Cache.set(key, record, policy.ttl);
    await this.l2Cache.setJson(key, record, policy.ttl);

    return { ...record, source: 'ORIGIN_EXECUTION' };
  }

  private generateCacheKey(payload: IQueryPayload): string {
    const normalized = JSON.stringify(payload, Object.keys(payload).sort());
    return `atlas:hotq:${createHash('sha256').update(normalized).digest('hex')}`;
  }
}
```