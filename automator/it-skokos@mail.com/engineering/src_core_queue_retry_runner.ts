# Atlas Core Retry Queue Implementation with Graceful Backoff and Telemetry
**Author:** Nyx Okafor  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D15 17:25  
**Inputs used:** Business Document (Company Document)  
## Summary

Engineered a resilient, human-centered retry queue for the Atlas Core background job runner, integrating exponential backoff with jitter and telemetry emissions aligned with SLA policies defined in Business Document: Company Document.

## Deliverable
```
/**
 * Atlas Core - Job Runner Retry Queue
 * Author: Nyx Okafor <nyx@itskokos.internal>
 * 
 * Grounded in the resiliency and customer-experience directives established in
 * 'Business Document: Company Document', this module ensures transient disruptions
 * do not degrade the tactile elegance of our user-facing SaaS and face-to-face service flows.
 */

import { EventEmitter } from 'events';

export interface JobPayload {
  id: string;
  tenantId: string;
  name: string;
  payload: Record<string, unknown>;
  attempt: number;
  maxRetries: number;
  nextRunAt: number;
}

export interface RetryConfig {
  baseDelayMs: number;
  maxDelayMs: number;
  jitterFactor: number;
}

export class RetryQueueManager extends EventEmitter {
  private queue: Map<string, JobPayload> = new Map();
  private config: RetryConfig;

  constructor(config?: Partial<RetryConfig>) {
    super();
    // Default intervals derived from Business Document: Company Document baseline SLAs
    this.config = {
      baseDelayMs: config?.baseDelayMs ?? 1000,
      maxDelayMs: config?.maxDelayMs ?? 30000,
      jitterFactor: config?.jitterFactor ?? 0.2,
    };
  }

  public scheduleRetry(job: JobPayload, error: Error): void {
    if (job.attempt >= job.maxRetries) {
      this.emit('job:exhausted', { job, error, timestamp: Date.now() });
      return;
    }

    const nextAttempt = job.attempt + 1;
    const delay = this.calculateBackoff(nextAttempt);
    const updatedJob: JobPayload = {
      ...job,
      attempt: nextAttempt,
      nextRunAt: Date.now() + delay,
    };

    this.queue.set(job.id, updatedJob);
    this.emit('job:retrying', { job: updatedJob, delay, reason: error.message });
  }

  private calculateBackoff(attempt: number): number {
    const rawBackoff = Math.min(this.config.maxDelayMs, this.config.baseDelayMs * Math.pow(2, attempt - 1));
    const jitter = rawBackoff * this.config.jitterFactor * (Math.random() * 2 - 1);
    return Math.max(this.config.baseDelayMs, Math.floor(rawBackoff + jitter));
  }

  public popReadyJobs(): JobPayload[] {
    const now = Date.now();
    const ready: JobPayload[] = [];
    for (const [id, job] of this.queue.entries()) {
      if (job.nextRunAt <= now) {
        ready.push(job);
        this.queue.delete(id);
      }
    }
    return ready;
  }
}
```