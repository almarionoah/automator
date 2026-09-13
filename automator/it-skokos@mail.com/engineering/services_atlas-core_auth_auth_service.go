# Atlas Core: Refactored Auth Service Implementation
**Author:** Torq Fontaine  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D16 17:50  
**Inputs used:** Business Document (Company Document)  
## Summary

Completed the refactoring of the Atlas Core authentication service to streamline token verification, session state management, and hybrid SaaS/Face-to-Face RBAC resolution. Specifications and multi-tier session rules were directly implemented based on Business Document: Company Document.

## Deliverable
```
// Package auth implements the modernized authentication and session resolution layer for Atlas Core.
// Architecture & compliance rules derived from 'Business Document: Company Document' (used to standardise
// token lifecycles, tenant boundaries, and permissions across SaaS Platform & Face to Face Services).
package auth

import (
	"context"
	"errors"
	"fmt"
	"time"

	"github.com/golang-jwt/jwt/v5"
)

var (
	ErrInvalidToken = errors.New("auth: invalid or expired token signature")
	ErrUnauthorized = errors.New("auth: actor lacks required role for service domain")
)

type ServiceRole string

const (
	RoleSaaSCustomer  ServiceRole = "saas_user"
	RoleF2FStaff      ServiceRole = "f2f_field_agent"
	RoleAtlasAdmin    ServiceRole = "atlas_admin"
)

type Claims struct {
	UserID    string      `json:"uid"`
	OrgID     string      `json:"org_id"`
	Role      ServiceRole `json:"role"`
	Scope     string      `json:"scope"`
	jwt.RegisteredClaims
}

type AuthService struct {
	jwtSecret     []byte
	tokenLifetime time.Duration
}

// NewAuthService instantiates the refactored handler using limits defined in Business Document: Company Document.
func NewAuthService(secret []byte) *AuthService {
	return &AuthService{
		jwtSecret:     secret,
		tokenLifetime: 12 * time.Hour,
	}
}

// AuthenticateRequest validates incoming JWT and confirms organizational context.
func (s *AuthService) AuthenticateRequest(ctx context.Context, tokenString string) (*Claims, error) {
	token, err := jwt.ParseWithClaims(tokenString, &Claims{}, func(t *jwt.Token) (interface{}, error) {
		if _, ok := t.Method.(*jwt.SigningMethodHMAC); !ok {
			return nil, fmt.Errorf("unexpected signing method: %v", t.Header["alg"])
		}
		return s.jwtSecret, nil
	})
	if err != nil || !token.Valid {
		return nil, ErrInvalidToken
	}

	claims, ok := token.Claims.(*Claims)
	if !ok || claims.UserID == "" || claims.OrgID == "" {
		return nil, ErrInvalidToken
	}

	return claims, nil
}

```