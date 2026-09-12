# Atlas Core: 30s Product Demo Spec & Storyboard
**Author:** Zed Petrov  
**Department:** Marketing  
**Project:** Atlas Core  
**Produced:** D145 08:30  
**Inputs used:** Git Access (Personal Access Token), Credentials (Git Hub Personal Access Token)  
## Summary

High-impact 30-second video demo script and asset-pull configuration for Atlas Core, focusing on edge-case platform resilience across hybrid SaaS and F2F workflows.

## Deliverable
```
# Project: Atlas Core — 30s Product Teaser (Marketing Demo Spec)
**Author:** Zed Petrov, Marketing (Edge-Case Specialist)
**Status:** Completed Artefact

## 1. Resource Integration & Asset Sourcing
- **Git Access: Personal Access Token**: Utilized to authenticate against internal UI component repos to extract the exact CSS tokens, SVG iconography, and telemetry state diagrams used in the visual overlays.
- **Credentials: Git Hub Personal Access Token**: Used to clone the staging deployment branch (`atlas-core/staging-v2.4`), allowing automated rendering of live dashboard animations and real-time F2F synchronization logs under high-latency edge cases.

## 2. 30-Second Video Script & Storyboard

| Time | Visual Track | Audio / Voiceover | On-Screen Text |
|---|---|---|---|
| 00:00 - 00:06 | Split-screen: High-volume SaaS web event queue vs. local F2F offline terminal syncing. | 'Data doesn't stop at the edge. When hybrid infrastructure stalls, Atlas Core takes over.' | **Atlas Core: Unbroken Flow** |
| 00:06 - 00:15 | Smooth UI zoom into Atlas Core telemetry panel showing sub-millisecond failover. | 'Engineered for extreme reliability: zero dropped frames, real-time sync, and millisecond edge resolution.' | **99.999% Resilience / Zero Drift** |
| 00:15 - 00:24 | Dynamic dynamic workflow graph switching instantly from cloud to offline F2F node. | 'Unified control for enterprise platforms and physical touchpoints, all in a single pane of glass.' | **SaaS + F2F Unified** |
| 00:24 - 00:30 | Sleek 3D logo resolve with animated CTA and enterprise trial link. | 'Scale without edge-case blind spots. Experience Atlas Core today.' | **Deploy Atlas Core Today -> it-skokos.com/atlas** |

## 3. Production Notes
- Render Engine: Remotion (React-driven video rendering via GitHub asset pipeline).
- Aspect Ratio: 16:9 (Primary) & 9:16 (Vertical Cut).
```