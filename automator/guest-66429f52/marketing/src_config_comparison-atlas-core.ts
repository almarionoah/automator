# Atlas Core Comparison Landing Page Edge-Case & Matrix Config
**Author:** Juno Bishop  
**Department:** Marketing  
**Project:** Atlas Core  
**Produced:** D152 23:35  
**Inputs used:** Git Access (Personal Access Token), Credentials (Git Hub Personal Access Token)  
## Summary

Production configuration, feature comparison matrix, and UTM edge-case handling for the newly deployed Atlas Core vs. Legacy comparison landing page, integrating both SaaS and F2F service tier differentials.

## Deliverable
```
/**
 * Project: Atlas Core - Comparison Landing Page Matrix
 * Author: Juno Bishop (Marketing / Growth Edge-Case Archaeologist)
 * Auth & CI Deployment Notes:
 * - Used 'Git Access: Personal Access Token' to clone and query internal benchmark metrics from the private it-skokos/marketing-data repo.
 * - Used 'Credentials: Git Hub Personal Access Token' to authenticate automated PR deployments against GitHub Enterprise actions for live preview generation.
 */

export interface ComparisonTier {
  feature: string;
  atlasCoreSaaS: string | boolean;
  atlasCoreF2F: string | boolean;
  legacyCompetitors: string | boolean;
  edgeCaseNotes: string;
}

export const AtlasCoreComparisonConfig = {
  slug: '/compare/atlas-core-vs-legacy',
  meta: {
    title: 'Atlas Core vs. Legacy SaaS & F2F Hybrid Solutions | I.T. Skokos',
    description: 'Detailed platform breakdown comparing Atlas Core automated SaaS workflows and on-site F2F integrations against legacy monolithic vendors.',
    canonicalFallback: 'https://itskokos.com/compare/atlas-core',
    utmEdgeCaseRouting: {
      stripMaliciousParams: true,
      preserveDeepLinkHash: true,
      unknownSourceRedirect: '/compare/atlas-core?ref=untracked_direct'
    }
  },
  featureMatrix: [
    {
      feature: 'Hybrid SaaS-to-F2F Escalation',
      atlasCoreSaaS: 'Native Dispatch',
      atlasCoreF2F: 'Included (SLA 2hr)',
      legacyCompetitors: '3rd-Party Ticket',
      edgeCaseNotes: 'Fails gracefully to localized phone routing if browser geolocation API is denied.'
    },
    {
      feature: 'Telemetry Rate Limiting',
      atlasCoreSaaS: 'Infinite Ingestion',
      atlasCoreF2F: 'Dedicated Field Proxy',
      legacyCompetitors: 'Hard Cap at 50k req/min',
      edgeCaseNotes: 'Accounts for high-burst telemetry during regional network partitions.'
    }
  ]
};
```