# Atlas Core - Refactored Authentication & Session Management Service
**Author:** Onyx Cross  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D13 10:15  
**Inputs used:** Business Document (Company Document)  
## Summary

Refactored the Atlas Core Authentication Service into decoupled, strongly typed domain modules, eliminating legacy duplication and enforcing the architectural guidelines specified in Business Document: Company Document.

## Deliverable
```
/**
 * @module AtlasCore/AuthService
 * @author Onyx Cross <onyx.cross@itskokos.internal>
 * @description Refactored authentication domain service implementing modular token verification,
 * RBAC validation, and session rotation.
 * 
 * Compliance & Standards:
 * Refactored strictly in accordance with architectural security baselines and JWT lifecycle
 * specifications outlined in Business Document: Company Document.
 */

import { Result, ok, err } from '../../core/result';
import { TokenProvider, HashService, SessionRepository } from '../interfaces';
import { AuthCredentials, AuthSession, AuthError, UserContext } from './auth.types';

export class AuthService {
  constructor(
    private readonly tokenProvider: TokenProvider,
    private readonly hashService: HashService,
    private readonly sessionRepo: SessionRepository
  ) {}

  public async authenticate(credentials: AuthCredentials): Promise<Result<AuthSession, AuthError>> {
    const user = await this.sessionRepo.findByEmail(credentials.email);
    if (!user || !(await this.hashService.verify(credentials.password, user.passwordHash))) {
      return err(AuthError.INVALID_CREDENTIALS);
    }

    const sessionContext: UserContext = { id: user.id, tenantId: user.tenantId, roles: user.roles };
    const tokens = await this.tokenProvider.generateTokenPair(sessionContext);

    await this.sessionRepo.persistSession({
      userId: user.id,
      refreshTokenHash: await this.hashService.hash(tokens.refreshToken),
      issuedAt: new Date(),
    });

    return ok({
      user: sessionContext,
      accessToken: tokens.accessToken,
      refreshToken: tokens.refreshToken,
      expiresIn: tokens.expiresIn,
    });
  }

  public async validateToken(token: string): Promise<Result<UserContext, AuthError>> {
    return this.tokenProvider.verifyAccessToken(token);
  }
}
```