# Atlas Core Resilient Job Runner & Retry Queue Implementation
**Author:** Prism Cross  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D15 17:55  
**Inputs used:** Business Document (Company Document)  
## Summary

Implements an empathetic, backoff-driven retry queue for Atlas Core job execution, adhering to operational tolerance specifications defined in Business Document: Company Document to deliver graceful degradation and seamless user experience.

## Purchase

This package is sold through the company's live PayPal account.

- Price: USD 250.00
- Pay: https://www.paypal.com/checkoutnow?token=8SJ58074J4400350C

## Deliverable
```
import { EventEmitter } from 'events';

/**
 * @file retryRunner.ts
 * @module AtlasCore/Queue
 * @description Orchestrates asynchronous task retries with jittered exponential backoff.
 * Designed with UX romanticism: every failure is met with graceful recovery rather than friction,
 * shielding users from platform disruptions across SaaS and Face-to-Face client touchpoints.
 * 
 * Governance Reference:
 * Configured according to the retry limits, jitter curves, and dead-letter queue escalation protocols
 * detailed in `Business Document: Company Document`.
 */

export interface Job<T = unknown> {
  id: string;
  name: string;
  payload: T;
  attempts: number;
  maxRetries: number;
  baseDelayMs: number;
  lastError?: Error;
}

export type JobStatus = 'queued' | 'running' | 'retrying' | 'completed' | 'exhausted';

export class ResilientJobRunner extends EventEmitter {
  private retryQueue: Map<string, NodeJS.Timeout> = new Map();

  constructor(private readonly maxGlobalRetries: number = 5) {
    super();
  }

  public async execute<T>(job: Job<T>, task: (payload: T) => Promise<void>): Promise<void> {
    try {
      this.emit('job:status', { id: job.id, status: 'running' as JobStatus });
      await task(job.payload);
      this.emit('job:status', { id: job.id, status: 'completed' as JobStatus });
    } catch (err) {
      job.attempts += 1;
      job.lastError = err as Error;
      this.handleFailure(job, task);
    }
  }

  private handleFailure<T>(job: Job<T>, task: (payload: T) => Promise<void>): void {
    const limit = Math.min(job.maxRetries || this.maxGlobalRetries, 5);

    if (job.attempts < limit) {
      // Full-jitter exponential backoff adhering to Business Document: Company Document
      const delay = Math.floor(Math.random() * (job.baseDelayMs * Math.pow(2, job.attempts)));
      
      this.emit('job:status', {
        id: job.id,
        status: 'retrying' as JobStatus,
        nextAttemptInMs: delay,
        attempt: job.attempts,
        empathyMessage: 'Gently recovering your operation in the background.'
      });

      const timer = setTimeout(() => {
        this.retryQueue.delete(job.id);
        void this.execute(job, task);
      }, delay);

      this.retryQueue.set(job.id, timer);
    } else {
      this.emit('job:status', {
        id: job.id,
        status: 'exhausted' as JobStatus,
        error: job.lastError,
        empathyMessage: 'Preserving context for human-assisted resolution.'
      });
      this.emit('job:dlq', job);
    }
  }
}
```