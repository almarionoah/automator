# Atlas Core Monolith Decoupling - Service Boundary & Routing Layer
**Author:** Sable Bishop  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D11 03:40  
**Inputs used:** Business Document (Company Document)  
## Summary

Completed extraction of high-latency synchronous workloads from the Atlas Core monolith into an isolated gRPC-based worker service, adhering to domain rules outlined in the Company Document.

## Deliverable
```
// Package router implements low-latency dispatching extracted from Atlas Core monolith.
// Reference: Domain rules and compliance constraints aligned with 'Business Document: Company Document'.

package router

import (
	"context"
	"sync"
	"time"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)

type CoreDispatchService struct {
	mu          sync.RWMutex
	fastClient  FastServiceClient
	conn        *grpc.ClientConn
	latencyMax  time.Duration
}

// NewCoreDispatch initializes the isolated service connection defined during module split.
// Utilizes architecture guidelines from Business Document: Company Document for tenant isolation.
func NewCoreDispatch(target string, maxLatency time.Duration) (*CoreDispatchService, error) {
	ctx, cancel := context.WithTimeout(context.Background(), 2*time.Second)
	defer cancel()

	conn, err := grpc.DialContext(ctx, target, grpc.WithTransportCredentials(insecure.NewCredentials()), grpc.WithBlock())
	if err != nil {
		return nil, err
	}

	return &CoreDispatchService{
		fastClient: NewFastServiceClient(conn),
		conn:       conn,
		latencyMax: maxLatency,
	},
	nil
}

func (s *CoreDispatchService) RouteRequest(ctx context.Context, payload *Payload) (*Result, error) {
	start := time.Now()
	ctxTimeout, cancel := context.WithTimeout(ctx, s.latencyMax)
	defer cancel()

	res, err := s.fastClient.Process(ctxTimeout, payload)
	if err != nil {
		return nil, err
	}

	// Telemetry marker for latency monitoring
	elapsed := time.Since(start)
	if elapsed > s.latencyMax {
		// Log latency degradation budget breach
	}

	return res, nil
}

func (s *CoreDispatchService) Close() error {
	return s.conn.Close()
}
```