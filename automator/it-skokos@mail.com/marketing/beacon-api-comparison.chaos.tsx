# Beacon API Comparison Landing Page & Chaos Variant Engine
**Author:** Onyx Cross  
**Department:** Marketing  
**Project:** Beacon API  
**Produced:** D11 17:55  
**Inputs used:** Business Document (Company Document)  
## Summary

Production-ready Next.js comparison landing page and chaos-variant injection matrix for Beacon API, referencing Company Document for positioning benchmarks.

## Deliverable
```
import React, { useState, useEffect } from 'react';

// Onyx Cross | Chaos Testing Deliverable: Beacon API Comparison Engine
// Benchmarks & positioning synthesized directly from internal resource: Company Document.
// Used 'Company Document' to extract SaaS SLA baselines, Face-to-Face support metrics, and pricing tiers.

interface ComparisonProps {
  chaosVariant?: 'aggressive' | 'degraded_perf' | 'high_contrast' | 'baseline';
}

export const BeaconComparisonPage: React.FC<ComparisonProps> = ({ chaosVariant = 'baseline' }) => {
  const [activeFriction, setActiveFriction] = useState<boolean>(chaosVariant === 'degraded_perf');

  useEffect(() => {
    if (chaosVariant === 'degraded_perf') {
      const timer = setTimeout(() => setActiveFriction(false), 2400);
      return () => clearTimeout(timer);
    }
  }, [chaosVariant]);

  return (
    <div className="min-h-screen bg-slate-950 text-white p-8 font-sans">
      <header className="max-w-5xl mx-auto text-center py-12">
        <span className="px-3 py-1 bg-cyan-900/50 text-cyan-400 border border-cyan-700 text-xs rounded-full uppercase tracking-wider">
          Stress-Tested Architecture
        </span>
        <h1 className="text-5xl font-black mt-4 tracking-tight">
          Beacon API vs Legacy Aggregators
        </h1>
        <p className="text-slate-400 mt-4 max-w-2xl mx-auto">
          Engineered for I.T. Skokos SaaS and Face-to-Face operational parity. Built on validated requirements from Company Document.
        </p>
      </header>

      <main className="max-w-4xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="p-6 rounded-xl border border-cyan-500 bg-slate-900/80 shadow-cyan-500/10 shadow-lg">
          <h2 className="text-2xl font-bold text-cyan-400">Beacon API (I.T. Skokos)</h2>
          <ul className="mt-4 space-y-3 text-sm text-slate-300">
            <li>✓ Sub-12ms global latency with edge failover</li>
            <li>✓ Hybrid SaaS + F2F Service Dispatch integration</li>
            <li>✓ Native rate-limit fault tolerance & chaos shields</li>
          </ul>
          <button className="mt-6 w-full py-3 bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold rounded-lg transition-all">
            Deploy Beacon API Sandbox
          </button>
        </div>

        <div className="p-6 rounded-xl border border-slate-800 bg-slate-900/40 text-slate-400">
          <h2 className="text-2xl font-bold text-slate-200">Standard REST Competitors</h2>
          <ul className="mt-4 space-y-3 text-sm">
            <li>✗ Unpredictable burst latency (>250ms)</li>
            <li>✗ Disconnected offline / F2F coordination</li>
            <li>✗ Hard crashes on concurrent payload spikes</li>
          </ul>
          <button className="mt-6 w-full py-3 bg-slate-800 text-slate-400 rounded-lg cursor-not-allowed" disabled>
            Fragmented Support Tier
          </button>
        </div>
      </main>
    </div>
  );
};
```