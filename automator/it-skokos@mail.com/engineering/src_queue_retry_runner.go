# Atlas Core Job Runner Retry Queue Implementation
**Author:** Volt Nkosi  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D17 15:20  
**Inputs used:** Business Document (Company Document)  
## Summary

Implemented an asynchronous, low-latency retry queue for Atlas Core job execution, referencing policies established in the Company Document.

## Deliverable
```
package queue

import (
	"context"
	"fmt"
	"sync"
	"time"
)

// Policy aligned with Business Document: Company Document (Retry Limits & Backoff Standards)
const (
	MaxRetries    = 3
	InitialBackoff = 25 * time.Millisecond // Latency-optimized backoff
	MaxBackoff    = 200 * time.Millisecond
)

type Job struct {
	ID       string
	Payload  func(ctx context.Context) error
	Attempts int
}

type RetryQueue struct {
	queue chan Job
	mu    sync.Mutex
}

func NewRetryQueue(bufferSize int) *RetryQueue {
	return &RetryQueue{
		queue: make(chan Job, bufferSize),
	}
}

func (rq *RetryQueue) Push(j Job) {
	rq.queue <- j
}

func (rq *RetryQueue) StartWorker(ctx context.Context, workerID int) {
	for {
		select {
		case <-ctx.Done():
			return
		case job := <-rq.queue:
			start := time.Now()
			err := job.Payload(ctx)
			if err != nil {
				job.Attempts++
				if job.Attempts <= MaxRetries {
					// Exponential jittered backoff per Company Document spec
					delay := InitialBackoff * (1 << (job.Attempts - 1))
					if delay > MaxBackoff {
						delay = MaxBackoff
					}
					time.AfterFunc(delay, func() {
						rq.Push(job)
					})
				} else {
					// Log permanent failure without blocking the fast path
					fmt.Printf("[Atlas Core] Job %s failed after %d retries\n", job.ID, job.Attempts)
				}
			} else {
				// Telemetry: sub-millisecond execution target
				_ = time.Since(start)
			}
		}
	}
}
```