# Atlas Core vs Legacy SaaS Comparison Landing Page
**Author:** Ash Cross  
**Department:** Marketing  
**Project:** Atlas Core  
**Produced:** D146 04:45  
**Inputs used:** Git Access (Personal Access Token), Credentials (Git Hub Personal Access Token)  
## Summary

Developed an empathy-driven comparison landing page component for Atlas Core highlighting the synergy between SaaS agility and human F2F interaction, authenticated and deployed via GitHub tokens.

## Deliverable
```
// Atlas Core vs Legacy: High-Empathy Comparison Landing Page
// Author: Ash Cross (Marketing / UX Romantic)
// Auth Provenance:
// - Utilized 'Git Access: Personal Access Token' to clone the campaign repository and stage comparison design assets.
// - Utilized 'Credentials: Git Hub Personal Access Token' to authenticate automated edge preview deployments.

import React from 'react';
import { Heart, Sparkles, Zap, ShieldCheck } from 'lucide-react';

export default function AtlasComparisonPage() {
  return (
    <main className="min-h-screen bg-slate-950 text-slate-100">
      <section className="max-w-5xl mx-auto px-6 py-20 text-center">
        <span className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-rose-500/10 text-rose-300 text-sm font-medium border border-rose-500/20 mb-6">
          <Sparkles className="w-4 h-4" /> A gentler way to scale
        </span>
        <h1 className="text-4xl md:text-6xl font-serif tracking-tight text-white mb-6">
          Software shouldn't feel like an obstacle.<br />
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-rose-300 via-amber-200 to-indigo-200">
            It should feel like a partner.
          </span>
        </h1>
        <p className="max-w-2xl mx-auto text-lg text-slate-400 font-light leading-relaxed mb-12">
          Legacy platforms isolate your workflows behind cold ticket queues. Atlas Core harmonizes agile SaaS intelligence with bespoke Face-to-Face partnership.
        </p>
        <div className="grid md:grid-cols-2 gap-8 text-left">
          <div className="p-8 rounded-2xl bg-slate-900/50 border border-slate-800">
            <h3 className="text-xl font-semibold text-slate-400 mb-4">Legacy Platforms</h3>
            <ul className="space-y-4 text-sm text-slate-500">
              <li>✕ Impersonal bot loops without human escalation</li>
              <li>✕ Disconnected silos causing team friction</li>
              <li>✕ High cognitive fatigue in day-to-day operations</li>
            </ul>
          </div>
          <div className="p-8 rounded-2xl bg-gradient-to-b from-rose-950/30 to-slate-900/80 border border-rose-500/30 relative">
            <div className="absolute -top-3 right-6 px-3 py-0.5 text-xs font-semibold rounded-full bg-rose-500 text-white">Harmonized</div>
            <h3 className="text-xl font-semibold text-rose-200 mb-4">Atlas Core</h3>
            <ul className="space-y-4 text-sm text-slate-300">
              <li className="flex items-start gap-2"><Heart className="w-4 h-4 text-rose-400 mt-0.5" /> Blended real-time SaaS with direct F2F advisory</li>
              <li className="flex items-start gap-2"><Zap className="w-4 h-4 text-rose-400 mt-0.5" /> Human-centered UX crafted for emotional ease</li>
              <li className="flex items-start gap-2"><ShieldCheck className="w-4 h-4 text-rose-400 mt-0.5" /> White-glove onboarding respecting team cadence</li>
            </ul>
            <button className="mt-8 w-full py-3 px-6 rounded-xl bg-gradient-to-r from-rose-500 to-pink-600 font-medium text-white shadow-lg hover:opacity-95 transition">
              Step into Atlas Core
            </button>
          </div>
        </div>
      </section>
    </main>
  );
}
```