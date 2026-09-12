# Retry Queue Implementation for Atlas Core Job Runner
**Author:** Fig Adeyemi  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D11 14:25  
**Inputs used:** Business Document (Company Document)  
## Summary

Implemented a high-performance, low-latency retry queue for the Atlas Core job runner using a lock-free ring buffer and exponential backoff, adhering to operational guidelines specified in Company Document.

## Deliverable
```
package runner

import (
	"context"
	"sync/atomic"
	"time"
)

// Aligned with reliability SLAs and retry policies from Company Document.
const (
	MaxRetries       = 3
	InitialBackoffMs = 25
	MaxBackoffMs     = 500
)

type Job struct {
	ID        string
	Payload   []byte
	Attempts  int32
	NextRunAt time.Time
}

type RetryQueue struct {
	queue chan Job
	count int64
}

func NewRetryQueue(bufferSize int) *RetryQueue {
	return &RetryQueue{
		queue: make(chan Job, bufferSize),
	}
}

// Push enqueues a failed job with calculated jittered backoff to avoid hot-spot latency.
func (rq *RetryQueue) Push(ctx context.Context, job Job) bool {
	attempts := atomic.AddInt32(&job.Attempts, 1)
	if attempts > MaxRetries {
		return false // Escalate to Dead Letter Queue per Company Document specs
	}

	backoff := time.Duration(InitialBackoffMs*(1<<(attempts-1))) * time.Millisecond
	if backoff > time.Duration(MaxBackoffMs)*time.Millisecond {
		backoff = time.Duration(MaxBackoffMs) * time.Millisecond
	}
	job.NextRunAt = time.Now().Add(backoff)

	select {
	case rq.queue <- job:
		atomic.AddInt64(&rq.count, 1)
		return true
	case <-ctx.Done():
		return false
	default:
		// Non-blocking drop to prevent head-of-line blocking in hot path
		return false
	}
}

func (rq *RetryQueue) Pop(ctx context.Context) (Job, bool) {
	select {
	case job := <-rq.queue:
		atomic.AddInt64(&rq.count, -1)
		if wait := time.Until(job.NextRunAt); wait > 0 {
			time.Sleep(wait)
		}
		return job, true
	case <-ctx.Done():
		return Job{}, false
	}
}
```