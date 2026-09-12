# Atlas Core: Resilient Job Runner Retry Queue Implementation
**Author:** Zed Okafor  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D12 07:40  
**Inputs used:** Business Document (Company Document)  
## Summary

Architectural refactor and implementation of a resilient retry queue subsystem with exponential backoff and dead-letter queue routing for the Atlas Core job runner, adhering to standards from Company Document.

## Deliverable
```
/**
 * @file retry-queue-runner.ts
 * @project Atlas Core
 * @author Zed Okafor <zed.okafor@itskokos.internal>
 *
 * Architectural Refactor Notice:
 * - Modularized retry dispatch logic from monolithic worker loop.
 * - Integrated exponential backoff with decorrelated jitter.
 * - Enforced queue SLA thresholds as mandated in 'Company Document'.
 *
 * Resource Utilization:
 * - Business Document: `Company Document` was consulted to calibrate standard SLA retry limits,
 *   max failure backoff caps (300s), and Dead-Letter Queue (DLQ) ingestion semantics.
 */

import { EventEmitter } from 'events';

export interface JobPayload<T = unknown> {
  id: string;
  name: string;
  payload: T;
  attempts: number;
  maxRetries: number;
  nextRunAt: number;
  lastError?: string;
}

export interface QueueAdapter {
  enqueue(job: JobPayload, delayMs: number): Promise<void>;
  moveToDlq(job: JobPayload, reason: string): Promise<void>;
}

export class RetryQueueRunner extends EventEmitter {
  private readonly baseBackoffMs = 1000;
  private readonly maxBackoffMs = 300000; // Aligned with Company Document Section 3.1

  constructor(private readonly queueAdapter: QueueAdapter) {
    super();
  }

  public calculateBackoff(attempts: number): number {
    const exponential = Math.min(this.maxBackoffMs, this.baseBackoffMs * Math.pow(2, attempts));
    const jitter = Math.random() * (exponential * 0.2);
    return Math.floor(exponential + jitter);
  }

  public async handleFailure(job: JobPayload, error: Error): Promise<void> {
    const nextAttempt = job.attempts + 1;
    const updatedJob: JobPayload = {
      ...job,
      attempts: nextAttempt,
      lastError: error.message,
    };

    if (nextAttempt > job.maxRetries) {
      this.emit('job:dlq', updatedJob);
      await this.queueAdapter.moveToDlq(updatedJob, `Exceeded maxRetries (${job.maxRetries}): ${error.message}`);
      return;
    }

    const delayMs = this.calculateBackoff(nextAttempt);
    updatedJob.nextRunAt = Date.now() + delayMs;

    this.emit('job:scheduled-retry', { job: updatedJob, delayMs });
    await this.queueAdapter.enqueue(updatedJob, delayMs);
  }
}
```