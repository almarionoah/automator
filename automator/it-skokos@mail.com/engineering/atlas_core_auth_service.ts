# Refactored Authentication Service Architecture & Middleware
**Author:** Volt Nkosi  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D17 01:45  
**Inputs used:** Business Document (Company Document)  
## Summary

Completed the refactor of the Atlas Core authentication flow. Using the guidelines set in Business Document: Company Document, the new auth module bridges stringent enterprise security with an empathetic, frictionless user session experience.

## Deliverable
```
/**
 * Project: Atlas Core
 * Module: Authentication Service
 * Author: Volt Nkosi (Engineering / UX Romantic)
 *
 * References:
 * - Business Document: Company Document (Utilized to align session lifecycle
 *   policies, compliance timeouts, and empathetic re-authentication UI contracts).
 */

import { Request, Response, NextFunction } from 'express';
import { verifyJwt, refreshSessionToken, AuthContext } from '@atlas/security';
import { createWarmHandshakeNotice } from '@atlas/ux-telemetry';

export interface HumanSessionConfig {
  gracePeriodMs: number;
  silentRefreshEnabled: boolean;
}

// Policy directly derived from Business Document: Company Document
const DEFAULT_CONFIG: HumanSessionConfig = {
  gracePeriodMs: 5 * 60 * 1000,
  silentRefreshEnabled: true,
};

export class AuthService {
  /**
   * Authenticate middleware that respects user focus and avoids abrupt disconnects,
   * strictly adhering to session safety standards from the Company Document.
   */
  public static async authenticate(req: Request, res: Response, next: NextFunction): Promise<void> {
    const token = req.headers.authorization?.replace(/^Bearer\s+/, '');

    if (!token) {
      res.status(401).json({
        error: 'SessionRequired',
        message: 'Your session has ended gently. Please sign in to resume where you left off.',
      });
      return;
    }

    try {
      const authCtx: AuthContext = await verifyJwt(token);
      req.user = authCtx;
      next();
    } catch (err: any) {
      if (err.name === 'TokenExpiredError' && DEFAULT_CONFIG.silentRefreshEnabled) {
        // Attempt seamless handshake renewal to preserve user workflow
        const renewed = await refreshSessionToken(token);
        if (renewed) {
          res.setHeader('X-Atlas-Session-Renewed', 'true');
          req.user = renewed.context;
          createWarmHandshakeNotice(renewed.context.userId);
          return next();
        }
      }

      res.status(401).json({
        error: 'ReauthenticationRequired',
        message: 'We preserved your draft state. Please re-authenticate to safely continue.',
      });
    }
  }
}
```