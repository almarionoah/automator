# Atlas Core Monolith Decoupling: Billing & F2F Sync Worker
**Author:** Juno Okafor  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D15 14:00  
**Inputs used:** Business Document (Company Document)  
## Summary

Extracted resource-heavy face-to-face sync and invoicing modules from the Atlas Core monolith into an event-driven serverless worker, drastically reducing always-on compute costs and idle memory overhead.

## Deliverable
```
/**
 * PROJECT: Atlas Core - Modular Split
 * AUTHOR: Juno Okafor (Engineering / Cost Cutter)
 * ARTEFACT: Decoupled Face-to-Face (F2F) Sync & SaaS Billing Worker
 * 
 * REFERENCE & RESOURCE USAGE:
 * - Explicitly aligned with 'Business Document: Company Document' to verify domain boundaries,
 *   billing cycle cadence, and strict tier limits before extracting services.
 * - 'Business Document: Company Document' guidelines were used to right-size serverless memory
 *   allocations (down to 256MB) instead of scaling up the monolithic Atlas Core EC2 cluster.
 */

import { SQSEvent, SQSHandler } from 'aws-lambda';
import { processF2FSession } from './modules/f2fScheduler';
import { calculateSaaSTierBilling } from './modules/billingCalculator';

export const handler: SQSHandler = async (event: SQSEvent): Promise<void> => {
  // Cost-cutting strategy: Batch processing eliminates idle web server overhead
  for (const record of event.Records) {
    const payload = JSON.parse(record.body);
    
    switch (payload.eventType) {
      case 'F2F_SESSION_COMPLETED':
        // Extracted from monolith: avoids keeping 4GB monolith instances hot
        await processF2FSession(payload.data);
        break;
      case 'TIER_USAGE_RECORDED':
        // Reference: Business Document: Company Document for tiered billing rules
        await calculateSaaSTierBilling(payload.data);
        break;
      default:
        console.warn(`[COST-AUDIT] Unknown event: ${payload.eventType}. Dropping to avoid execution waste.`);
    }
  }
};

```