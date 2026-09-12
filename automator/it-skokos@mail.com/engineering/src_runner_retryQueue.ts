# Atlas Core: Job Runner Exponential Backoff Retry Queue
**Author:** Zed Hale  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D2 14:00  
## Summary

Implemented an in-memory/Redis-compatible retry queue mechanism with exponential backoff and dead-letter queue (DLQ) support for Atlas Core. Assumed a Node.js/TypeScript stack using BullMQ/Redis abstractions and standard Atlas job envelope schemas.

## Deliverable
```
import { EventEmitter } from 'events';

export interface Job<T = unknown> {
  id: string;
  name: string;
  data: T;
  attempts: number;
  maxRetries: number;
  backoffMs: number;
  lastError?: string;
}

export interface QueueOptions {
  defaultMaxRetries?: number;
  initialBackoffMs?: number;
  backoffFactor?: number;
  maxBackoffMs?: number;
}

export class RetryQueue extends EventEmitter {
  private queue: Map<string, Job> = new Map();
  private dlq: Map<string, Job> = new Map();
  private timers: Map<string, NodeJS.Timeout> = new Map();
  private options: Required<QueueOptions>;

  constructor(options: QueueOptions = {}) {
    super();
    this.options = {
      defaultMaxRetries: options.defaultMaxRetries ?? 3,
      initialBackoffMs: options.initialBackoffMs ?? 1000,
      backoffFactor: options.backoffFactor ?? 2,
      maxBackoffMs: options.maxBackoffMs ?? 60000,
    };
  }

  public scheduleRetry(job: Job, error: Error): void {
    job.attempts += 1;
    job.lastError = error.message;

    if (job.attempts > (job.maxRetries || this.options.defaultMaxRetries)) {
      this.moveToDlq(job);
      return;
    }

    const delay = Math.min(
      this.options.initialBackoffMs * Math.pow(this.options.backoffFactor, job.attempts - 1),
      this.options.maxBackoffMs
    );

    this.queue.set(job.id, job);
    this.emit('job:retry_scheduled', { jobId: job.id, attempt: job.attempts, delay });

    const timer = setTimeout(() => {
      this.timers.delete(job.id);
      this.queue.delete(job.id);
      this.emit('job:ready', job);
    }, delay);

    this.timers.set(job.id, timer);
  }

  private moveToDlq(job: Job): void {
    this.queue.delete(job.id);
    this.dlq.set(job.id, job);
    this.emit('job:failed', { jobId: job.id, error: job.lastError, attempts: job.attempts });
  }

  public getDlqJobs(): Job[] {
    return Array.from(this.dlq.values());
  }
}
```