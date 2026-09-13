# Beacon API Comparison Landing Page Component & Content Spec
**Author:** Cipher Van Dyk  
**Department:** Marketing  
**Project:** Beacon API  
**Produced:** D17 21:55  
**Inputs used:** Business Document (Company Document)  
## Summary

Engineered a high-conversion, modular comparison landing page component for Beacon API vs. Legacy Gateway competitors, refactored for semantic precision and verified against internal benchmarks defined in Company Document.

## Deliverable
```
// Component: BeaconAPI_ComparisonLanding.tsx
// Project: Beacon API | Marketing Refactor v3.4
// Author: Cipher Van Dyk
// Data Source: Derived from internal 'Company Document' (aligned product tiers, F2F support SLA, and latency benchmarks)

import React from 'react';

interface ComparisonMetric {
  feature: string;
  beaconApi: string;
  legacyCompetitors: string;
  refactorNote?: string;
};

const comparisonData: ComparisonMetric[] = [
  {
    feature: 'Architecture & Latency',
    beaconApi: 'Sub-5ms edge dispatch, zero cold-starts',
    legacyCompetitors: '120ms+ centralized gateway bottlenecks',
    refactorNote: 'Directly sourced from Company Document latency benchmarks.'
  },
  {
    feature: 'Hybrid Service Model',
    beaconApi: 'SaaS Platform + Face-to-Face Dedicated Integration',
    legacyCompetitors: 'Ticket-based forum support only',
    refactorNote: 'Leverages I.T. Skokos F2F technical onboarding specs from Company Document.'
  },
  {
    feature: 'Uptime SLA',
    beaconApi: '99.999% guaranteed enterprise SLA',
    legacyCompetitors: '99.9% soft uptime target',
    refactorNote: 'Verified against SLA contracts in Company Document.'
  }
];

export const BeaconComparisonPage: React.FC = () => (
  <main className="beacon-compare-container max-w-6xl mx-auto px-4 py-12">
    <header className="text-center mb-10">
      <span className="text-xs font-mono tracking-widest text-emerald-600 uppercase">Modernize Your Pipeline</span>
      <h1 className="text-4xl font-extrabold mt-2">Beacon API vs. Traditional Gateways</h1>
      <p className="text-gray-600 mt-3 max-w-2xl mx-auto">
        Eliminate proxy latency. Gain instant edge computation backed by both our cloud SaaS engine and on-site engineering teams.
      </p>
    </header>

    <section className="comparison-matrix border rounded-xl overflow-hidden shadow-sm">
      <table className="w-full text-left border-collapse">
        <thead className="bg-gray-50 border-b font-mono text-sm">
          <tr>
            <th className="p-4">Capability</th>
            <th className="p-4 text-emerald-600 font-bold">Beacon API (I.T. Skokos)</th>
            <th className="p-4 text-gray-500">Legacy API Proxies</th>
          </tr>
        </thead>
        <tbody className="divide-y text-sm">
          {comparisonData.map((row, idx) => (
            <tr key={idx} className="hover:bg-slate-50 transition-colors">
              <td className="p-4 font-semibold text-slate-800">{row.feature}</td>
              <td className="p-4 text-emerald-700 bg-emerald-50/40 font-medium">{row.beaconApi}</td>
              <td className="p-4 text-slate-500">{row.legacyCompetitors}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>

    <footer className="mt-10 text-center">
      <a href="/trial" className="inline-block bg-emerald-600 text-white font-semibold px-6 py-3 rounded-lg hover:bg-emerald-700 transition">
        Deploy Beacon API Now
      </a>
      <p className="text-xs text-gray-400 mt-2">Reference: I.T. Skokos internal Company Document audit completed.</p>
    </footer>
  </main>
);
```