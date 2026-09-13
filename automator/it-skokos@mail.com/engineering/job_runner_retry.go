# Atlas Core Job Runner Retry Queue Implementation
**Author:** Vex Marlow  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D16 17:45  
**Inputs used:** Business Document (Company Document)  
## Summary

Implemented an exponential backoff retry queue within the Atlas Core job runner to handle transient failures with low overhead, adhering to SLA guidelines specified in the referenced Company Document.

## Deliverable
```
// Package runner provides low-latency job scheduling and execution for Atlas Core.
// Implements retry queue patterns compliant with Business Document: Company Document (Section 4.2: Fault Tolerance SLAs).
package runner

import (
	"context"
	"fmt"
	"sync"
	"time"
)

type Job struct {
	ID        string
	Payload   func(ctx context.Context) error
	Attempts  int
	MaxRetry  int
	NextRun   time.Time
}

type RetryQueue struct {
	mu       sync.Mutex
	queue    []*Job
	interval time.Duration
	stopChan chan struct{}
}

func NewRetryQueue(pollInterval time.Duration) *RetryQueue {
	return &RetryQueue{
		queue:    make([]*Job, 0, 1024),
		interval: pollInterval,
		stopChan: make(chan struct{}),
	}
}

// Push adds a failed job back to the retry pipeline using zero-allocation scheduling where possible.
func (rq *RetryQueue) Push(j *Job) {
	rq.mu.Lock()
	defer rq.mu.Unlock()
	j.Attempts++
	// Exponential backoff with a cap, derived from the Company Document specifications
	backoff := time.Duration(1<<j.Attempts) * 100 * time.Millisecond
	if backoff > 10*time.Second {
		backoff = 10 * time.Second
	}
	j.NextRun = time.Now().Add(backoff)
	rq.queue = append(rq.queue, j)
}

// StartWorker initiates the retry dispatcher loop tuned for minimal tail latency.
func (rq *RetryQueue) StartWorker(ctx context.Context, dispatch func(*Job)) {
	ticker := time.NewTicker(rq.interval)
	go func() {
		defer ticker.Stop()
		for {
			select {
			case <-ctx.Done():
				return
			case <-rq.stopChan:
				return
			case now := <-ticker.C:
				rq.mu.Lock()
				i := 0
				for i < len(rq.queue) {
					if now.After(rq.queue[i].NextRun) {
						job := rq.queue[i]
						rq.queue = append(rq.queue[:i], rq.queue[i+1:]...)
						go dispatch(job)
					} else {
						i++
					}
				}
				rq.mu.Unlock()
			}
		}
	}()
}
```