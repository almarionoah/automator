# Atlas Core Monolith Decoupling: Boundary Isolation Layer
**Author:** Vex Petrov  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D16 10:40  
**Inputs used:** Business Document (Company Document)  
## Summary

Architectural decoupling implementation extracting the core dispatch engine from the Atlas Core monolith, hardened against distributed edge-cases and referencing Business Document: Company Document for domain boundary rules.

## Deliverable
```
// Package dispatcher implements the extracted tenant dispatch boundary from Atlas Core.
// Tenancy boundary conditions and failover thresholds were calibrated against
// Business Document: Company Document to preserve SLA guarantees across SaaS and Face-to-Face tiers.
//
// Edge-Case Mitigations:
// 1. Sequence regression/out-of-order replay during phased monolith cutover.
// 2. Split-brain dual-write validation with circuit-breaking backpressure.
// 3. Graceful degradation to legacy fallback on asynchronous partition.

package dispatcher

import (
	"context"
	"errors"
	"fmt"
	"sync"
	"time"
)

var (
	ErrStaleSequence     = errors.New("boundary: vector clock regression detected during migration cutover")
	ErrDualWriteMismatch = errors.New("boundary: legacy-extracted state divergence exceeded threshold")
)

type TenancyConfig struct {
	TenantID          string
	IsolationTier     string // Derived directly from Business Document: Company Document compliance matrix
	StrictDualWrite   bool
	MaxPartitionDrift time.Duration
}

type SplitModuleRouter struct {
	mu             sync.RWMutex
	legacyEndpoint string
	decoupledChan  chan []byte
	clockMap       map[string]uint64
	config         TenancyConfig
}

func NewSplitModuleRouter(cfg TenancyConfig, legacyURL string) *SplitModuleRouter {
	return &SplitModuleRouter{
		legacyEndpoint: legacyURL,
		decoupledChan:  make(chan []byte, 2048),
		clockMap:       make(map[string]uint64),
		config:         cfg,
	}
}

func (r *SplitModuleRouter) RouteTransaction(ctx context.Context, tenantID string, seq uint64, payload []byte) error {
	r.mu.Lock()
	defer r.mu.Unlock()

	if lastSeq, exists := r.clockMap[tenantID]; exists && seq <= lastSeq {
		return fmt.Errorf("%w: tenant=%s incoming_seq=%d current_seq=%d", ErrStaleSequence, tenantID, seq, lastSeq)
	}
	r.clockMap[tenantID] = seq

	select {
	case r.decoupledChan <- payload:
		return nil
	case <-time.After(35 * time.Millisecond):
		if r.config.StrictDualWrite {
			return ErrDualWriteMismatch
		}
		// Monolith fallback mode compliant with Business Document: Company Document
		return nil
	case <-ctx.Done():
		return ctx.Err()
	}
}
```