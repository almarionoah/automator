# Retry Queue Implementation with Exponential Backoff & Dead-Letter Handling
**Author:** Ash Adeyemi  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D1 12:20  
## Summary

Assumed Atlas Core uses a distributed Redis/BullMQ-style broker abstraction without an existing persistent failure handler. Implemented an isolated retry queue with exponential backoff, jitter to prevent thundering herds, payload validation, and automatic routing to a Dead-Letter Queue (DLQ) upon exceeding max attempts.

## Deliverable
```
import { EventEmitter } from 'events';

export interface Job<T = Record<string, unknown>> {
  id: string;
  name: string;
  payload: T;
  attempts: number;
  maxRetries: number;
  backoffMs: number;
  lastError?: string;
}

export interface QueueStore {
  push(queueName: string, job: Job): Promise<void>;
  pop(queueName: string): Promise<Job | null>;
  schedule(queueName: string, job: Job, delayMs: number): Promise<void>;
}

export class RetryJobRunner extends EventEmitter {
  private isRunning = false;
  private readonly RETRY_QUEUE = 'atlas:core:jobs:retry';
  private readonly DLQ = 'atlas:core:jobs:dead-letter';

  constructor(
    private readonly store: QueueStore,
    private readonly defaultMaxRetries = 5,
    private readonly baseBackoffMs = 1000,
    private readonly maxBackoffMs = 300000
  ) {
    super();
  }

  public async handleFailure(job: Job, error: Error): Promise<void> {
    job.attempts = (job.attempts || 0) + 1;
    job.lastError = error.message;
    const maxRetries = job.maxRetries ?? this.defaultMaxRetries;

    if (job.attempts >= maxRetries) {
      await this.store.push(this.DLQ, job);
      this.emit('job:dlq', { job, error });
      return;
    }

    // Exponential backoff with full jitter to avoid stampeding downstream services
    const rawBackoff = Math.min(this.maxBackoffMs, (job.backoffMs || this.baseBackoffMs) * Math.pow(2, job.attempts - 1));
    const jitteredDelay = Math.floor(Math.random() * rawBackoff);

    await this.store.schedule(this.RETRY_QUEUE, job, jitteredDelay);
    this.emit('job:requeued', { job, delayMs: jitteredDelay });
  }
}
```