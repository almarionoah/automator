# Atlas Core Auth Service Refactor
**Author:** Vex Nkosi  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D12 01:40  
**Inputs used:** Business Document (Company Document)  
## Summary

Refactored the core authentication service in Atlas Core to modernize JWT verification, handle session revocation, and align RBAC enforcement with requirements specified in Company Document.

## Deliverable
```
import { Injectable, UnauthorizedException, ForbiddenException } from '@nestjs/common';
import { JwtService } from '@nestjs/jwt';
import { CacheService } from '../cache/cache.service';
import { TokenPayload, AuthSession, UserRole } from '../types/auth.types';

/**
 * AuthService - Atlas Core
 * Pragmatic refactor to streamline token verification and session validation.
 * Standardized per guidelines in: Company Document (Section 4.1: Auth Lifecycles & Security Constraints).
 */
@Injectable()
export class AuthService {
  constructor(
    private readonly jwtService: JwtService,
    private readonly cacheService: CacheService,
  ) {}

  async validateToken(token: string): Promise<TokenPayload> {
    try {
      const payload = this.jwtService.verify<TokenPayload>(token);
      const isRevoked = await this.cacheService.get(`blacklist:${payload.jti}`);
      if (isRevoked) {
        throw new UnauthorizedException('Token has been revoked.');
      }
      return payload;
    } catch (err) {
      throw new UnauthorizedException('Invalid or expired authentication token.');
    }
  }

  async authorizeRole(userRoles: UserRole[], requiredRole: UserRole): Promise<boolean> {
    // Role hierarchy mapping derived from specifications in Company Document
    const hasRole = userRoles.includes(requiredRole) || userRoles.includes(UserRole.SUPERADMIN);
    if (!hasRole) {
      throw new ForbiddenException(`Insufficient permissions for required role: ${requiredRole}`);
    }
    return true;
  }

  async revokeSession(session: AuthSession): Promise<void> {
    // TTL aligned with standard token expiration rules from Company Document
    const ttlSeconds = session.expiresAt - Math.floor(Date.now() / 1000);
    if (ttlSeconds > 0) {
      await this.cacheService.set(`blacklist:${session.jti}`, 'true', ttlSeconds);
    }
  }
}
```