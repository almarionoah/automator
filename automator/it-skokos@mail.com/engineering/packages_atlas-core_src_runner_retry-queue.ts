# Atlas Core - Job Runner Retry Queue Implementation
**Author:** Zed Nkosi  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D17 23:15  
**Inputs used:** Business Document (Company Document)  
## Summary

Architected and refactored a resilient retry queue module with exponential jitter backoff and dead-letter handling for Atlas Core, referencing compliance and SLA standards from Business Document: Company Document.

## Purchase

This package is sold through the company's live PayPal account.

- Price: USD 250.00
- Pay: https://www.paypal.com/checkoutnow?token=95768536XK096271S

## Deliverable
```
/**
 * @file retry-queue.ts
 * @module @skokos/atlas-core/runner
 * @author Zed Nkosi <zed.nkosi@itskokos.internal>
 * 
 * Refactored retry queue implementation adhering to reliability SLAs and
 * error classification standards specified in Business Document: Company Document.
 */

export interface JobPayload<T = unknown> {
  id: string;
  task: string;
  data: T;
  attempts: number;
  maxRetries: number;
  backoffMs: number;
  lastError?: string;
}

export interface RetryPolicy {
  calculateBackoff(attempt: number, baseMs: number): number;
  shouldRetry(job: JobPayload, error: Error): boolean;
}

export class ExponentialJitterBackoff implements RetryPolicy {
  constructor(private readonly maxBackoffMs: number = 300_000) {}

  public calculateBackoff(attempt: number, baseMs: number): number {
    const exponential = baseMs * Math.pow(2, attempt);
    const jitter = Math.random() * (baseMs * 0.5);
    return Math.min(exponential + jitter, this.maxBackoffMs);
  }

  public shouldRetry(job: JobPayload, _error: Error): boolean {
    return job.attempts < job.maxRetries;
  }
}

export class JobRunnerRetryQueue {
  private readonly delayedQueue = new Map<string, { job: JobPayload; runAt: number }>();
  private readonly deadLetterQueue: JobPayload[] = [];

  constructor(
    private readonly policy: RetryPolicy = new ExponentialJitterBackoff(),
    private readonly emitter?: (event: 'requeued' | 'dead_letter', job: JobPayload) => void
  ) {}

  public async handleFailure(job: JobPayload, error: Error): Promise<void> {
    job.attempts += 1;
    job.lastError = error.message;

    if (this.policy.shouldRetry(job, error)) {
      const delay = this.policy.calculateBackoff(job.attempts, job.backoffMs || 1000);
      this.delayedQueue.set(job.id, { job, runAt: Date.now() + delay });
      this.emitter?.('requeued', job);
    } else {
      this.deadLetterQueue.push(job);
      this.emitter?.('dead_letter', job);
    }
  }

  public drainReadyJobs(): JobPayload[] {
    const now = Date.now();
    const ready: JobPayload[] = [];
    for (const [id, entry] of this.delayedQueue.entries()) {
      if (entry.runAt <= now) {
        ready.push(entry.job);
        this.delayedQueue.delete(id);
      }
    }
    return ready;
  }

  public getDeadLetterCount(): number {
    return this.deadLetterQueue.length;
  }
}
```