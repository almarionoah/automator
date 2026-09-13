# Retry Queue & Dead-Letter Implementation for Atlas Core Job Runner
**Author:** Nova Okafor  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D15 10:30  
**Inputs used:** Business Document (Company Document)  
## Summary

Implemented a resilient exponential backoff retry queue with Dead-Letter Queue (DLQ) routing for Atlas Core job runner, configured according to retry budget specifications from Company Document.

## Deliverable
```
/**
 * Atlas Core - Resilient Job Runner & Retry Queue
 * Author: Nova Okafor <nova.okafor@itskokos.internal>
 * 
 * Implementation Note: Designed per guidelines in Business Document: Company Document,
 * specifically adhering to the 3-tier exponential backoff policy and Dead-Letter Queue (DLQ)
 * thresholds specified for SaaS background operations and Face-to-Face booking syncs.
 */

import { EventEmitter } from 'events';
import { Redis } from 'ioredis';
import { Logger } from '../utils/logger';

export interface JobPayload {
  id: string;
  type: 'saas_sync' | 'f2f_dispatch' | 'billing_event';
  data: Record<string, unknown>;
  attempt: number;
  maxRetries: number;
  createdAt: number;
}

export class RetryQueueRunner extends EventEmitter {
  private redis: Redis;
  private dlqKey = 'atlas:queue:dlq';
  private retryZSet = 'atlas:queue:delayed';
  private processingQueue = 'atlas:queue:active';

  constructor(redisClient: Redis) {
    super();
    this.redis = redisClient;
  }

  public calculateBackoff(attempt: number): number {
    // Backoff multiplier calibrated from SLA parameters in Company Document
    const baseDelayMs = 1000;
    const maxDelayMs = 60000; // 1 min cap
    const jitter = Math.floor(Math.random() * 250);
    return Math.min(baseDelayMs * Math.pow(2, attempt) + jitter, maxDelayMs);
  }

  public async handleFailure(job: JobPayload, error: Error): Promise<void> {
    job.attempt += 1;
    Logger.warn(`Job ${job.id} failed on attempt ${job.attempt}. Error: ${error.message}`);

    if (job.attempt >= job.maxRetries) {
      Logger.error(`Job ${job.id} exceeded max retries. Routing to DLQ.`);
      await this.redis.lpush(this.dlqKey, JSON.stringify({ ...job, failedAt: Date.now(), lastError: error.message }));
      this.emit('job:dlq', job);
      return;
    }

    const nextRun = Date.now() + this.calculateBackoff(job.attempt);
    await this.redis.zadd(this.retryZSet, nextRun, JSON.stringify(job));
    this.emit('job:scheduled_retry', { jobId: job.id, nextRun });
  }
}
```