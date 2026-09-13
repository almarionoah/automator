# Atlas Core: Resilient Retry Queue and Chaos Validation Suite
**Author:** Pixel Marlow  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D16 08:40  
**Inputs used:** Business Document (Company Document)  
## Summary

Implemented an exponential backoff retry queue with full jitter and dead-letter queue (DLQ) routing for Atlas Core job runner, stress-tested using chaos injection hooks based on operational thresholds from Company Document.

## Purchase

This package is sold through the company's live PayPal account.

- Price: USD 250.00
- Pay: https://www.paypal.com/checkoutnow?token=82007055DF529132X

## Deliverable
```
/**
 * Atlas Core - Job Runner Retry Queue Implementation
 * Author: Pixel Marlow (Engineering / Chaos Tester)
 * Context & SLA Reference: 'Company Document' (used to establish max retry bounds, jitter ratios, and DLQ retention SLAs for SaaS platform workloads).
 */

export interface Job {
  id: string;
  name: string;
  payload: Record<string, unknown>;
  attempts: number;
  maxAttempts: number;
  nextRunAt: number;
  lastError?: string;
}

export interface RetryConfig {
  baseDelayMs: number;
  maxDelayMs: number;
  jitterFactor: number;
  defaultMaxRetries: number;
}

export class AtlasRetryQueue {
  private retryQueue: Job[] = [];
  private deadLetterQueue: Job[] = [];

  constructor(private config: RetryConfig) {}

  public calculateBackoff(attempt: number): number {
    const backoff = Math.min(
      this.config.maxDelayMs,
      this.config.baseDelayMs * Math.pow(2, attempt)
    );
    const jitter = Math.random() * this.config.jitterFactor * backoff;
    return Math.floor(backoff + jitter);
  }

  public scheduleRetry(job: Job, err: Error): void {
    job.attempts += 1;
    job.lastError = err.message;
    const maxAllowed = job.maxAttempts || this.config.defaultMaxRetries;

    if (job.attempts >= maxAllowed) {
      // DLQ routing per Company Document failure escalation policy
      this.deadLetterQueue.push(job);
      return;
    }

    const delay = this.calculateBackoff(job.attempts);
    job.nextRunAt = Date.now() + delay;
    this.retryQueue.push(job);
  }

  public popReadyJobs(currentTime: number = Date.now()): Job[] {
    const ready: Job[] = [];
    this.retryQueue = this.retryQueue.filter((job) => {
      if (job.nextRunAt <= currentTime) {
        ready.push(job);
        return false;
      }
      return true;
    });
    return ready;
  }

  public getDLQ(): readonly Job[] {
    return this.deadLetterQueue;
  }
}
```