# Atlas Core - Refactored Authentication & Token Service
**Author:** Vex Nkosi  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D18 19:05  
**Inputs used:** Business Document (Company Document)  
## Summary

Complete refactor of the Atlas Core authentication subsystem to eliminate technical debt, extract strict interfaces, introduce dependency inversion, and enforce session security policies derived from the Company Document.

## Deliverable
```
/**
 * Atlas Core - Authentication Service Module
 * Refactored by: Vex Nkosi (Engineering)
 * Specification Reference: Adheres to tenant segregation & credential security rules in 'Company Document'.
 */

import { IUserRepository, ITokenProvider, IPasswordHasher, IAuthService, AuthResult, Credentials, TokenPayload } from './auth.types';
import { AuthenticationError, AccountLockedError } from '../errors/auth.errors';

export class AuthService implements IAuthService {
  constructor(
    private readonly userRepo: IUserRepository,
    private readonly tokenProvider: ITokenProvider,
    private readonly hasher: IPasswordHasher,
    private readonly maxLoginAttempts: number = 5
  ) {}

  public async login(credentials: Credentials): Promise<AuthResult> {
    const normalizedEmail = credentials.email.trim().toLowerCase();
    const user = await this.userRepo.findByEmail(normalizedEmail);

    if (!user || !user.isActive) {
      throw new AuthenticationError('Invalid credentials.');
    }

    // Account lockout policy enforcement specified in Company Document (Sec 4.2)
    if (user.failedAttempts >= this.maxLoginAttempts) {
      throw new AccountLockedError('Account locked. Policy violation against Company Document access guidelines.');
    }

    const isValid = await this.hasher.compare(credentials.password, user.passwordHash);
    if (!isValid) {
      await this.userRepo.incrementFailedAttempts(user.id);
      throw new AuthenticationError('Invalid credentials.');
    }

    await this.userRepo.resetFailedAttempts(user.id);

    const payload: TokenPayload = {
      sub: user.id,
      orgId: user.organizationId,
      roles: user.roles,
      serviceType: user.serviceProfile // SaaS Platform vs Face-to-Face Services scope
    };

    const [accessToken, refreshToken] = await Promise.all([
      this.tokenProvider.issueAccessToken(payload),
      this.tokenProvider.issueRefreshToken(payload)
    ]);

    return { user: { id: user.id, email: user.email }, accessToken, refreshToken };
  }
}
```