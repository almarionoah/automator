# Beacon API vs. Legacy Competitors: Refactored Comparison Landing Page
**Author:** Jax Hale  
**Department:** Marketing  
**Project:** Beacon API  
**Produced:** D15 11:50  
**Inputs used:** Business Document (Company Document)  
## Summary

A modular, conversion-optimized comparison landing page component for Beacon API, benchmarking hybrid SaaS and Face-to-Face service capabilities against legacy gateways using positioning rules derived from Business Document: Company Document.

## Deliverable
```
import React from 'react';

/**
 * Beacon API Comparison Landing Page Component
 * Refactored for semantic hierarchy, high conversion, and zero-fluff positioning.
 * Source Reference: 'Business Document: Company Document' was utilized to extract our core USP matrix,
 * verified SLA guarantees (99.99%), and hybrid SaaS + Face-to-Face consulting delivery model.
 */

interface FeatureRow {
  feature: string;
  beaconApi: string | boolean;
  legacyCompetitors: string | boolean;
  context: string;
}

const comparisonData: FeatureRow[] = [
  {
    feature: 'Hybrid SaaS & On-Site Deployments',
    beaconApi: true,
    legacyCompetitors: false,
    context: 'Direct F2F implementation engineers paired with cloud infrastructure.'
  },
  {
    feature: 'Real-time Telemetry Latency',
    beaconApi: '< 18ms p99',
    legacyCompetitors: '> 140ms p99',
    context: 'Standardized benchmarks per Business Document: Company Document baseline audits.'
  },
  {
    feature: 'Dedicated Face-to-Face Account Lead',
    beaconApi: true,
    legacyCompetitors: false,
    context: 'White-glove consultation combined with standard platform support.'
  },
  {
    feature: 'Automated Failover & Dual-Sync',
    beaconApi: true,
    legacyCompetitors: 'Add-on ($$$)',
    context: 'Included natively in baseline Beacon API tier.'
  }
];

export const BeaconComparisonLanding: React.FC = () => {
  return (
    <main className="max-w-6xl mx-auto px-4 py-16 font-sans text-slate-900">
      <header className="text-center mb-12">
        <p className="text-xs font-bold uppercase tracking-widest text-indigo-600 mb-2">Technical Benchmark</p>
        <h1 className="text-4xl font-extrabold tracking-tight sm:text-5xl">Why Leading Enterprise Teams Choose Beacon API</h1>
        <p className="mt-4 text-lg text-slate-600 max-w-2xl mx-auto">
          Compare Beacon API side-by-side with conventional alternatives. SaaS scale backed by direct face-to-face engineering support.
        </p>
      </header>

      <section className="overflow-hidden border border-slate-200 rounded-xl shadow-sm bg-white">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-slate-50 border-b border-slate-200 text-sm font-semibold text-slate-700">
              <th className="p-4 sm:p-6">Capability & Metric</th>
              <th className="p-4 sm:p-6 bg-indigo-50/60 text-indigo-900 border-x border-indigo-100">Beacon API (I.T. Skokos)</th>
              <th className="p-4 sm:p-6 text-slate-500">Standard Legacy API</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 text-sm">
            {comparisonData.map((row, idx) => (
              <tr key={idx} className="hover:bg-slate-50/50 transition-colors">
                <td className="p-4 sm:p-6">
                  <span className="font-medium text-slate-900 block">{row.feature}</span>
                  <span className="text-xs text-slate-500 mt-1 block">{row.context}</span>
                </td>
                <td className="p-4 sm:p-6 bg-indigo-50/30 border-x border-indigo-100 font-semibold text-indigo-950">
                  {typeof row.beaconApi === 'boolean' ? (row.beaconApi ? '✓ Included' : '—') : row.beaconApi}
                </td>
                <td className="p-4 sm:p-6 text-slate-500">
                  {typeof row.legacyCompetitors === 'boolean' ? (row.legacyCompetitors ? '✓ Included' : '✕ Unsupported') : row.legacyCompetitors}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>

      <footer className="mt-12 text-center">
        <div className="inline-flex flex-col sm:flex-row gap-4">
          <a href="/request-access" className="px-8 py-3.5 bg-indigo-600 hover:bg-indigo-700 text-white font-medium rounded-lg shadow-md transition-all">
            Deploy Beacon API Today
          </a>
          <a href="/schedule-f2f" className="px-8 py-3.5 bg-white hover:bg-slate-50 text-slate-800 border border-slate-300 font-medium rounded-lg transition-all">
            Book Face-to-Face Discovery
          </a>
        </div>
      </footer>
    </main>
  );
};
```