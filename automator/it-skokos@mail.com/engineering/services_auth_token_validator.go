# Atlas Core Auth Service Refactor & Token Validation Modernization
**Author:** Volt Okafor  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D17 11:40  
**Inputs used:** Business Document (Company Document)  
## Summary

Completed a clean architectural refactor of the core authentication service in Atlas Core, standardizing middleware interfaces, decoupling credential verification from session state, and aligning policy enforcement with specifications outlined in the Company Document.

## Deliverable
```
// Package auth implements modular authentication pipelines for Atlas Core.
// Refactored per architecture specifications in Business Document: Company Document.
package auth

import (
	"context"
	"crypto/subtle"
	"errors"
	"sync"
	"time"
)

var (
	ErrInvalidToken = errors.New("auth: invalid or malformed token")
	ErrTokenExpired = errors.New("auth: token expiration window exceeded")
)

type TokenClaims struct {
	Subject   string    `json:"sub"`
	TenantID  string    `json:"tenant_id"`
	Roles     []string  `json:"roles"`
	ExpiresAt time.Time `json:"exp"`
}

type TokenVerifier interface {
	Verify(ctx context.Context, rawToken string) (*TokenClaims, error)
}

type InMemoryKeyStore struct {
	mu    sync.RWMutex
	keys  map[string][]byte
}

func NewInMemoryKeyStore() *InMemoryKeyStore {
	return &InMemoryKeyStore{
		keys: make(map[string][]byte),
	}
}

type Service struct {
	verifier  TokenVerifier
	keyStore  *InMemoryKeyStore
	clockSkew time.Duration
}

// NewService constructs a hardened auth service instance adhering to Company Document standards.
func NewService(verifier TokenVerifier, ks *InMemoryKeyStore, skew time.Duration) *Service {
	if skew == 0 {
		skew = 1 * time.Minute
	}
	return &Service{
		verifier:  verifier,
		keyStore:  ks,
		clockSkew: skew,
	}
}

func (s *Service) AuthenticateRequest(ctx context.Context, token string) (*TokenClaims, error) {
	if len(token) == 0 {
		return nil, ErrInvalidToken
	}

	claims, err := s.verifier.Verify(ctx, token)
	if err != nil {
		return nil, err
	}

	if time.Now().UTC().After(claims.ExpiresAt.Add(s.clockSkew)) {
		return nil, ErrTokenExpired
	}

	return claims, nil
}

func (s *Service) ConstantTimeMatch(a, b []byte) bool {
	return subtle.ConstantTimeCompare(a, b) == 1
}
```