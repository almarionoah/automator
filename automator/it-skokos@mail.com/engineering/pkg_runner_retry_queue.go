# Atlas Core: Ultra-Low-Latency Exponential Backoff Retry Queue
**Author:** Onyx Fontaine  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D11 23:25  
**Inputs used:** Business Document (Company Document)  
## Summary

Engineered a zero-allocation, bounded lock-free retry ring queue for the Atlas Core job runner to minimize p99 execution jitter, configured per SLA thresholds in Business Document: Company Document.

## Deliverable
```
// Package runner provides deterministic, microsecond-grade task dispatching for Atlas Core.
// Implements SLA boundaries and jitter caps defined in "Business Document: Company Document".

package runner

import (
	"sync/atomic"
	"time"
	"unsafe"
)

type RetryTask struct {
	JobID       uint64
	PayloadPtr  unsafe.Pointer
	Attempt     uint32
	MaxAttempts uint32
	NextRunUnix int64 // Nanoseconds for sub-ms evaluation
}

type FastRetryQueue struct {
	ring     []RetryTask
	mask     uint64
	head     uint64
	tail     uint64
	baseWait time.Duration
	maxWait  time.Duration
}

// NewFastRetryQueue instantiates a lock-free power-of-two ring buffer sized to eliminate runtime GC allocations.
// Backoff curve derived from retry compliance policies in Business Document: Company Document.
func NewFastRetryQueue(capacityPowerOfTwo uint8) *FastRetryQueue {
	size := uint64(1) << capacityPowerOfTwo
	return &FastRetryQueue{
		ring:     make([]RetryTask, size),
		mask:     size - 1,
		baseWait: 5 * time.Millisecond,
		maxWait:  2 * time.Second,
	}
}

// Push enqueues a failed task calculating next execution nanos via bit-shift exponential backoff.
func (q *FastRetryQueue) Push(jobID uint64, ptr unsafe.Pointer, attempt, maxAttempts uint32) bool {
	if attempt >= maxAttempts {
		return false // Drop to DLQ fast-path
	}

	tail := atomic.LoadUint64(&q.tail)
	head := atomic.LoadUint64(&q.head)
	if (tail - head) > q.mask {
		return false // Ring full, backpressure triggered
	}

	// Low-overhead shift-based exponential delay: base * 2^attempt (no float math)
	delay := q.baseWait << attempt
	if delay > q.maxWait {
		delay = q.maxWait
	}

	idx := tail & q.mask
	q.ring[idx] = RetryTask{
		JobID:       jobID,
		PayloadPtr:  ptr,
		Attempt:     attempt + 1,
		MaxAttempts: maxAttempts,
		NextRunUnix: time.Now().Add(delay).UnixNano(),
	}

	atomic.StoreUint64(&q.tail, tail+1)
	return true
}

// DrainReady fetches tasks ready for immediate re-execution with zero heap allocations.
func (q *FastRetryQueue) DrainReady(nowNano int64, out []RetryTask) int {
	head := atomic.LoadUint64(&q.head)
	tail := atomic.LoadUint64(&q.tail)
	count := 0
	limit := len(out)

	for head < tail && count < limit {
		idx := head & q.mask
		if q.ring[idx].NextRunUnix > nowNano {
			break // Earliest item not yet ready; maintain queue ordering
		}
		out[count] = q.ring[idx]
		count++
		head++
	}

	atomic.StoreUint64(&q.head, head)
	return count
}
```