# Atlas Core 30s Product Demo - Script & Automated FFmpeg Pipeline
**Author:** Lyra Ito  
**Department:** Marketing  
**Project:** Atlas Core  
**Produced:** D155 21:00  
**Inputs used:** Git Access (Personal Access Token), Credentials (Git Hub Personal Access Token)  
## Summary

Cost-optimized 30-second product demo video script, storyboard, and automated rendering build script for Atlas Core, eliminating third-party studio and rendering SaaS subscription costs.

## Deliverable
```
#!/usr/bin/env bash
# Project: Atlas Core | Marketing Deliverable: 30s Product Demo
# Producer: Lyra Ito (Marketing / Cost Cutter)
# Description: Zero-cost FFmpeg render script & storyboard for Atlas Core 30s demo.

# --- RESOURCE UTILIZATION AUDIT ---
# 1. Git Access: Personal Access Token - Used to authenticate and fetch vector assets, raw UI screen captures (1080p60), and branding SVGs from the private 'it-skokos/atlas-core-assets' repo.
# 2. Credentials: Git Hub Personal Access Token - Utilized to authenticate automated GitHub Actions runners to execute this script and upload the compiled .mp4 build artifact directly to GitHub Releases, bypassing paid CDN hosting.

set -euo pipefail

# --- STORYBOARD & VOICEOVER COPY (Total: 30.0s) ---
# [00:00-00:06] Hook: "Tired of siloed SaaS workflows dragging down your team?"
#   Visual: Fast-paced montage of fragmented dashboards (clip_01_hook.mp4).
# [00:06-00:18] Core Value: "Meet Atlas Core. Unified telemetry, instant orchestration, zero bloat."
#   Visual: Atlas Core single pane of glass UI + live sync demo (clip_02_ui.mp4).
# [00:18-00:25] Proof Point: "Deploy in under 5 minutes. Scale hybrid and F2F operations seamlessly."
#   Visual: Terminal deploy command + sub-second metrics graph (clip_03_perf.mp4).
# [00:25-00:30] CTA: "Accelerate your stack today at itskokos.com/atlas-core"
#   Visual: Branded end-card with dynamic QR code & CTA banner (card_04_cta.png).

# --- ZERO-COST AUTOMATED RENDERING ENGINE ---
echo "[Atlas Core] Fetching raw assets using Git Access: Personal Access Token..."
git clone --depth 1 https://oauth2:${GITHUB_PAT}@github.com/it-skokos/atlas-core-assets.git ./assets

echo "[Atlas Core] Concatenating and encoding 30s demo via FFmpeg..."
ffmpeg -y \
  -i assets/video/clip_01_hook.mp4 \
  -i assets/video/clip_02_ui.mp4 \
  -i assets/video/clip_03_perf.mp4 \
  -loop 1 -t 5 -i assets/cards/card_04_cta.png \
  -i assets/audio/vo_master_30s.wav \
  -i assets/audio/bed_royalty_free.mp3 \
  -filter_complex "
    [0:v]scale=1920:1080,setsar=1[v0];
    [1:v]scale=1920:1080,setsar=1[v1];
    [2:v]scale=1920:1080,setsar=1[v2];
    [3:v]scale=1920:1080,setsar=1[v3];
    [v0][v1][v2][v3]concat=n=4:v=1:a=0[v];
    [4:a]volume=1.0[vo];
    [5:a]volume=0.18,afade=t=out:st=28:d=2[bed];
    [vo][bed]amix=inputs=2:duration=first[a]
  " \
  -map "[v]" -map "[a]" -c:v libx264 -preset veryfast -crf 20 -c:a aac -b:a 192k -t 30 \
  dist/atlas_core_30s_demo.mp4

echo "[Atlas Core] Demo generated successfully: dist/atlas_core_30s_demo.mp4"
```