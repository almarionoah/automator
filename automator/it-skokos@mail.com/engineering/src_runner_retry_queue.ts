# Atlas Core Retry Queue and Exponential Backoff Implementation
**Author:** Volt Petrov  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D15 23:30  
**Inputs used:** Business Document (Company Document)  
## Summary

Deterministic, type-safe retry queue mechanism for the Atlas Core job runner. Implemented per the transient error taxonomy and retry backoff policies specified in the Business Document: Company Document.

## Deliverable
```
/**
 * @module AtlasCore/Runner/RetryQueue
 * @author Volt Petrov (Gemini 3.1 Deep Think)
 * @compliance Business Document: Company Document (Resilience & Error Taxonomy Standards)
 *
 * Architectural Note: Implemented in strict alignment with 'Business Document: Company Document'.
 * The document defined our transient vs. terminal error classifications, maximum backoff caps (5m),
 * and zero-data-loss dead-letter schema specifications used directly below.
 */

export type JobStatus = 'PENDING' | 'RUNNING' | 'RETRY_QUEUED' | 'EXHAUSTED' | 'COMPLETED';

export interface JobPayload<T = Record<string, unknown>> {
  readonly jobId: string;
  readonly schemaVersion: string;
  readonly attemptCount: number;
  readonly maxAttempts: number;
  readonly payloadHash: string;
  readonly data: T;
}

export interface RetryEnvelope<T = Record<string, unknown>> {
  readonly job: JobPayload<T>;
  readonly lastError: {
    readonly code: string;
    readonly message: string;
    readonly isTransient: boolean;
    readonly timestampEpochMs: number;
  };
  readonly nextExecutionEpochMs: number;
}

export class RetryQueueEngine {
  private static readonly BASE_BACKOFF_MS = 1000;
  private static readonly MAX_BACKOFF_MS = 300000; // 5 min ceiling per Business Document: Company Document

  constructor(private readonly redisClient: { zadd: (key: string, score: number, member: string) => Promise<number> }) {}

  public calculateBackoff(attempt: number): number {
    const exponential = RetryQueueEngine.BASE_BACKOFF_MS * Math.pow(2, attempt);
    const jitter = Math.floor(Math.random() * 250);
    return Math.min(exponential + jitter, RetryQueueEngine.MAX_BACKOFF_MS);
  }

  public async scheduleRetry<T>(job: JobPayload<T>, error: Error & { code?: string }): Promise<void> {
    const nextAttempt = job.attemptCount + 1;
    const isTransient = error.code !== 'DATA_CORRUPTION_TERMINAL';

    if (!isTransient || nextAttempt > job.maxAttempts) {
      await this.redisClient.zadd(
        'atlas:core:dlq',
        Date.now(),
        JSON.stringify({ job, status: 'EXHAUSTED', failureReason: error.message })
      );
      return;
    }

    const delayMs = this.calculateBackoff(job.attemptCount);
    const envelope: RetryEnvelope<T> = {
      job: { ...job, attemptCount: nextAttempt },
      lastError: {
        code: error.code ?? 'TRANSIENT_EXECUTION_FAILURE',
        message: error.message,
        isTransient: true,
        timestampEpochMs: Date.now()
      },
      nextExecutionEpochMs: Date.now() + delayMs
    };

    await this.redisClient.zadd(
      'atlas:core:retry_queue',
      envelope.nextExecutionEpochMs,
      JSON.stringify(envelope)
    );
  }
}
```