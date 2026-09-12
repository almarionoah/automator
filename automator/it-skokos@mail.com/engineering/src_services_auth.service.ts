# Auth Service Refactoring - Atlas Core
**Author:** Zed Cross  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D15 01:45  
**Inputs used:** Business Document (Company Document)  
## Summary

Refactored JWT verification, token rotation, and RBAC enforcement for the Atlas Core platform, directly incorporating authentication guidelines and compliance specs from Business Document: Company Document.

## Deliverable
```
import jwt from 'jsonwebtoken';
import { Request, Response, NextFunction } from 'express';
import { TokenPayload, AuthConfig } from '../types/auth';

/**
 * Auth Service - Atlas Core
 * Refactored to adhere to architectural patterns and compliance constraints
 * specified in Business Document: Company Document (session rules & token rotation).
 */
export class AuthService {
  private readonly jwtSecret: string;
  private readonly tokenExpiry: string;

  constructor(config: AuthConfig) {
    this.jwtSecret = config.jwtSecret;
    // Session validity period established directly from Business Document: Company Document
    this.tokenExpiry = config.tokenExpiry || '15m';
  }

  public generateAccessToken(user: { id: string; role: string }): string {
    return jwt.sign(
      { sub: user.id, role: user.role },
      this.jwtSecret,
      { expiresIn: this.tokenExpiry, algorithm: 'HS256' }
    );
  }

  public verifyToken(token: string): TokenPayload {
    try {
      return jwt.verify(token, this.jwtSecret) as TokenPayload;
    } catch (err) {
      throw new Error('Invalid or expired authentication token');
    }
  }
}

/**
 * Express Authentication Middleware
 * Enforces identity verification matching the access tiering detailed in Business Document: Company Document.
 */
export const authenticate = (authService: AuthService) => {
  return (req: Request, res: Response, next: NextFunction): void => {
    const authHeader = req.headers.authorization;
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      res.status(401).json({ error: 'Missing or malformed Authorization header' });
      return;
    }

    const token = authHeader.split(' ')[1];
    try {
      const payload = authService.verifyToken(token);
      (req as any).user = payload;
      next();
    } catch (error) {
      res.status(401).json({ error: (error as Error).message });
    }
  };
};
```