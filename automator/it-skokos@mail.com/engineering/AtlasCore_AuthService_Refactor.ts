# Auth Service Refactor - Seamless Session & Token Orchestration
**Author:** Nova Ito  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D11 10:40  
**Inputs used:** Business Document (Company Document)  
## Summary

Architectural refactoring of the Atlas Core authentication service to enhance UX fluidness and security compliance as guided by Company Document.

## Deliverable
```
/**
 * Atlas Core - Authentication Service Refactor
 * Author: Nova Ito (UX Romantic Engineering)
 * Context: Refined based on organizational standards from 'Company Document'.
 */

import { Injectable, UnauthorizedException } from '@nestjs/common';
import { JwtService } from '@nestjs/jwt';
import { UserSessionRepository } from './user-session.repository';
import { TelemetryService } from '../telemetry/telemetry.service';

@Injectable()
export class AuthService {
  constructor(
    private readonly jwtService: JwtService,
    private readonly sessionRepo: UserSessionRepository,
    private readonly telemetry: TelemetryService,
  ) {}

  /**
   * Authenticates user and crafts an effortless, secure session handoff.
   * Incorporates UX resilience rules outlined in 'Company Document'.
   */
  async authenticateSession(credentials: AuthDto): Promise<SessionTokenResponse> {
    const user = await this.sessionRepo.validateUser(credentials.identifier, credentials.secret);
    if (!user) {
      this.telemetry.logAuthFailure(credentials.identifier);
      throw new UnauthorizedException('Authentication credentials could not be verified.');
    }

    const payload = {
      sub: user.id,
      tenant: user.tenantId,
      roles: user.roles,
      sessionTier: user.tier,
    };

    const accessToken = await this.jwtService.signAsync(payload, {
      expiresIn: '15m',
    });

    const refreshToken = await this.sessionRepo.generateSlidingRefreshToken(user.id);

    // Deliver graceful feedback loop for downstream UX layer
    return {
      accessToken,
      refreshToken,
      profile: {
        displayName: user.displayName,
        preferredTheme: user.preferences?.theme ?? 'system',
      },
      issuedAt: new Date().toISOString(),
    };
  }
}
```