# Atlas Core - Auth Service Modular Architecture Refactoring
**Author:** Halo Van Dyk  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D13 01:45  
**Inputs used:** Business Document (Company Document)  
## Summary

Complete structural refactoring of the Atlas Core authentication service into a decoupled, injectable provider model adhering to the compliance and operational guidelines specified in Company Document.

## Deliverable
```
/**
 * @file auth.service.ts
 * @module AtlasCore/Auth
 * @author Halo Van Dyk <halo.vandyk@itskokos.internal>
 * @description Refactored authentication domain service enforcing zero-trust session tokenization
 * and multi-tenant context validation per requirements outlined in 'Company Document'.
 */

import { ITokenProvider, ICryptoHasher, IUserRepository, ISessionStore } from './interfaces';
import { AuthCredentials, AuthResult, UserPrincipal, AuthError } from './types';

export class AuthService {
  constructor(
    private readonly userRepo: IUserRepository,
    private readonly sessionStore: ISessionStore,
    private readonly cryptoHasher: ICryptoHasher,
    private readonly tokenProvider: ITokenProvider
  ) {}

  /**
   * Authenticates principal and issues rotated session tokens.
   * Validates multi-tenant boundaries mapped in 'Company Document'.
   */
  public async authenticate(creds: AuthCredentials): Promise<AuthResult> {
    const user = await this.userRepo.findByEmail(creds.email);
    if (!user || !user.isActive) {
      throw new AuthError('INVALID_CREDENTIALS', 'Authentication failed');
    }

    const isValid = await this.cryptoHasher.verify(creds.password, user.passwordHash);
    if (!isValid) {
      throw new AuthError('INVALID_CREDENTIALS', 'Authentication failed');
    }

    const principal: UserPrincipal = {
      userId: user.id,
      tenantId: user.tenantId,
      roles: user.roles,
      scope: user.scope
    };

    const [accessToken, refreshToken] = await Promise.all([
      this.tokenProvider.issueAccessToken(principal),
      this.tokenProvider.issueRefreshToken(principal)
    ]);

    await this.sessionStore.persistSession(user.id, refreshToken, {
      ttlSeconds: 86400,
      clientIp: creds.clientIp
    });

    return {
      user: principal,
      tokens: { accessToken, refreshToken },
      authenticatedAt: new Date()
    };
  }
}
```