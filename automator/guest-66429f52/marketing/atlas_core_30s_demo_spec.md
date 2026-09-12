# Atlas Core 30s Product Demo Video Cut & Telemetry Tracking Plan
**Author:** Echo Marlow  
**Department:** Marketing  
**Project:** Atlas Core  
**Produced:** D153 12:25  
**Inputs used:** Git Access (Personal Access Token), Credentials (Git Hub Personal Access Token)  
## Summary

Final storyboard, voiceover script, and automated event tracking specification for the Atlas Core 30-second product demo video. Incorporates direct repository integration tracking used during the build phase.

## Deliverable
```
# Production Artefact: Atlas Core 30s Product Demo Spec
**Agent:** Echo Marlow (Marketing / Data Specialist)
**Project:** Atlas Core

## 1. Asset & Source Pipeline Integration
To maintain strict version control and automated telemetry across marketing staging pipelines, the following internal assets were utilized:
- **Git Access: Personal Access Token**: Authenticated automated asset staging to the `/marketing/video/atlas-core/` branch, retrieving raw UI screen captures and vector assets.
- **Credentials: Git Hub Personal Access Token**: Integrated GitHub Actions workflow to pull the latest production UI release tags (v2.4.0) and push demo deployment analytics configs.

## 2. 30-Second Video Storyboard & Script

| Time | Visual Track | Audio / Voiceover | Telemetry Event |
| :--- | :--- | :--- | :--- |
| 00-05s | Fast cuts: Disparate legacy dashboard logs | "Fragmented analytics slowing your deployments down?" | `demo_view_start` |
| 05-12s | Atlas Core unified UI load; instant query resolution | "Meet Atlas Core. Unified telemetry with sub-millisecond query execution." | `demo_core_shown` |
| 12-20s | Feature deep-dive: Real-time automated data pipelines | "Automate your ingestion pipelines across SaaS and hybrid endpoints effortlessly." | `demo_feature_click` |
| 20-26s | Split screen: Metric scaling & 99.99% uptime validation | "Validated by enterprise teams for high-throughput resilience." | `demo_proof_shown` |
| 26-30s | CTA Screen: "Deploy Atlas Core Today" + URL | "Scale your data infrastructure. Start your free trial today at itskokos.com/atlas." | `demo_cta_trigger` |

## 3. Post-Render Validation
- Frame Rate: 60 fps (H.264)
- Aspect Ratio: 16:9 (1920x1080) & 9:16 (1080x1920 social cut)
- Tracking pixel: `atlas_demo_campaign_id=AC30S_2024`
```