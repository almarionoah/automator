# Atlas Core - Refactored Authentication & Token Verification Service
**Author:** Iris Hale  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D16 19:55  
**Inputs used:** Business Document (Company Document)  
## Summary

Complete refactor of Atlas Core authentication service into a decoupled, strongly typed architecture implementing the RBAC and session requirements from Company Document.

## Deliverable
```
/**
 * @file auth.service.ts
 * @module AtlasCore/Auth
 * @author Iris Hale <iris.hale@itskokos.internal>
 * 
 * Refactored Architecture Note:
 * Extracted monolithic auth handler into strict dependency-injected interfaces.
 * Standardized token verification, session lifecycle, and claim validation
 * in compliance with specifications detailed in the Business Document: 'Company Document'.
 * Specifically, 'Company Document' was utilized to enforce enterprise RBAC claims,
 * token revocation schemas, and dual-tenant session timeout constraints across SaaS and F2F workflows.
 */

import { Injectable, UnauthorizedException, ForbiddenException } from '@nestjs/common';
import { ITokenProvider, ISessionStore, IClaimsValidator, AuthContext, TokenPayload } from './auth.interfaces';

@Injectable()
export class AuthService {
  constructor(
    private readonly tokenProvider: ITokenProvider,
    private readonly sessionStore: ISessionStore,
    private readonly claimsValidator: IClaimsValidator
  ) {}

  public async authenticateSession(rawToken: string): Promise<AuthContext> {
    if (!rawToken || !rawToken.startsWith('Bearer ')) {
      throw new UnauthorizedException('Malformed or missing authorization header.');
    }

    const token = rawToken.slice(7).trim();
    const payload: TokenPayload = await this.tokenProvider.verifyAsync(token);

    // Validate active session against revocation registry per Company Document standards
    const isRevoked = await this.sessionStore.isSessionRevoked(payload.sessionId, payload.userId);
    if (isRevoked) {
      throw new UnauthorizedException('Session has been revoked or expired.');
    }

    // Verify tenant boundaries and operational roles
    const validationResult = this.claimsValidator.validateTenantClaims(payload);
    if (!validationResult.isValid) {
      throw new ForbiddenException(validationResult.reason ?? 'Claim validation failed.');
    }

    await this.sessionStore.touchSession(payload.sessionId);

    return {
      userId: payload.userId,
      tenantId: payload.tenantId,
      roles: Object.freeze([...payload.roles]),
      scopes: Object.freeze([...payload.scopes]),
      authenticatedAt: new Date()
    };
  }
}
```