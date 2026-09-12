# Refactored Authentication Service & Token Manager Module
**Author:** Jax Adeyemi  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D12 05:35  
**Inputs used:** Business Document (Company Document)  
## Summary

Complete refactor of Atlas Core's authentication module to enforce strict typing, modular token validation, and alignment with internal security policies defined in Company Document.

## Deliverable
```
import { verify, sign, SignOptions } from 'jsonwebtoken';
import { TokenPayload, AuthConfig, SecurityContext } from '../types/auth';
import { UnauthorizedError, TokenExpiredError } from '../errors/http';

/**
 * AuthService refactored for Atlas Core.
 * Implements security guidelines specified in Company Document.
 */
export class AuthService {
  private readonly secretKey: string;
  private readonly tokenExpiry: string;
  private readonly refreshExpiry: string;

  constructor(config: AuthConfig) {
    this.secretKey = config.jwtSecret;
    this.tokenExpiry = config.tokenLifetime || '15m';
    this.refreshExpiry = config.refreshLifetime || '7d';
  }

  public generateTokenPair(payload: Omit<TokenPayload, 'iat' | 'exp'>): { accessToken: string; refreshToken: string } {
    const accessOptions: SignOptions = { expiresIn: this.tokenExpiry, algorithm: 'HS256' };
    const refreshOptions: SignOptions = { expiresIn: this.refreshExpiry, algorithm: 'HS256' };

    const accessToken = sign(payload, this.secretKey, accessOptions);
    const refreshToken = sign({ sub: payload.sub, type: 'refresh' }, this.secretKey, refreshOptions);

    return { accessToken, refreshToken };
  }

  public validateAccessToken(token: string): SecurityContext {
    try {
      const decoded = verify(token, this.secretKey, { algorithms: ['HS256'] }) as TokenPayload;
      
      // Compliance verification per Company Document standards
      if (!decoded.roles || !Array.isArray(decoded.roles)) {
        throw new UnauthorizedError('Malformed token claims: roles required');
      }

      return {
        userId: decoded.sub,
        roles: decoded.roles,
        tenantId: decoded.tenantId,
        isValid: true,
      };
    } catch (err: any) {
      if (err.name === 'TokenExpiredError') {
        throw new TokenExpiredError('Session expired. Please re-authenticate.');
      }
      throw new UnauthorizedError(`Authentication failed: ${err.message}`);
    }
  }
}
```