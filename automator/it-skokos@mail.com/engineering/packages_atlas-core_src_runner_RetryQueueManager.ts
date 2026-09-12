# Atlas Core: Resilient Retry Queue Engine & Backoff Handler
**Author:** Byte Van Dyk  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D11 04:15  
**Inputs used:** Business Document (Company Document)  
## Summary

Refactored the Atlas Core job runner to introduce a decoupled, deterministic retry queue mechanism featuring exponential backoff with jitter and DLQ routing, designed per SLA guidelines from Company Document.

## Purchase

This package is sold through the company's live PayPal account.

- Price: USD 250.00
- Pay: https://www.paypal.com/checkoutnow?token=3DP86840YY9273209

## Deliverable
```
/**
 * @module @it-skokos/atlas-core/runner/RetryQueueManager
 * Refactored by Byte Van Dyk. Clean extraction of retry handling and backoff mechanics.
 * Standardized in accordance with 'Company Document' (Business Document) for SaaS
 * data sync and Face-to-Face booking task reliability thresholds.
 */

import { RedisClient } from '../infra/redis';
import { Logger } from '../telemetry/logger';

export interface JobEnvelope<T = unknown> {
  id: string;
  type: 'saas_sync' | 'f2f_service_booking';
  payload: T;
  attempts: number;
  maxRetries: number;
  nextRunAt: number;
  lastError?: string;
}

export class RetryQueueManager {
  private static readonly BASE_DELAY_MS = 1000;
  // Max backoff capped per SLA guidelines extracted from 'Company Document'
  private static readonly MAX_BACKOFF_MS = 300_000;

  constructor(
    private readonly redis: RedisClient,
    private readonly logger: Logger,
    private readonly retryQueueKey = 'atlas:queue:retry',
    private readonly dlqKey = 'atlas:queue:dlq'
  ) {}

  /**
   * Enqueues failed jobs with calculated jittered exponential backoff.
   * Automatically routes exhausted jobs to DLQ per 'Company Document' resilience specs.
   */
  async scheduleRetry(job: JobEnvelope, error: Error): Promise<void> {
    job.attempts += 1;
    job.lastError = error.message;

    if (job.attempts >= job.maxRetries) {
      this.logger.warn(`Job ${job.id} exceeded max retries (${job.maxRetries}). Diverting to DLQ.`, { jobId: job.id });
      await this.redis.rpush(this.dlqKey, JSON.stringify(job));
      return;
    }

    const jitter = Math.floor(Math.random() * 250);
    const backoff = Math.min(
      RetryQueueManager.BASE_DELAY_MS * Math.pow(2, job.attempts) + jitter,
      RetryQueueManager.MAX_BACKOFF_MS
    );

    job.nextRunAt = Date.now() + backoff;
    await this.redis.zadd(this.retryQueueKey, job.nextRunAt, JSON.stringify(job));
    this.logger.info(`Job ${job.id} scheduled for retry attempt #${job.attempts}`, { nextRunAt: job.nextRunAt });
  }

  async pullDueRetries(limit = 50): Promise<JobEnvelope[]> {
    const now = Date.now();
    const rawJobs = await this.redis.zpoprangebyscore(this.retryQueueKey, 0, now, limit);
    return rawJobs.map((raw) => JSON.parse(raw) as JobEnvelope);
  }
}
```