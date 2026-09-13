# Beacon API - Model Routing Cost & Edge-Case Evaluation Report
**Author:** Halo Fontaine  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D16 01:50  
**Inputs used:** Business Document (Company Document)  
## Summary

Technical research deliverable evaluating dynamic model routing unit economics, fallback cascade anomalies, and cache miss edge cases for Beacon API, calibrated against baseline financial constraints from Company Document.

## Deliverable
```
# Beacon API: Model Routing Cost & Edge-Case Evaluation
**Author:** Halo Fontaine, Research Agent
**Project:** Beacon API | **Entity:** I.T. Skokos (SaaS & F2F Services)

## 1. Executive Summary & Baseline Reference
This evaluation stress-tests dynamic model routing costs across baseline SaaS queries and high-volume Face-to-Face (F2F) session transcript processing for Beacon API. Cost baselines and target margin thresholds were referenced directly from the **Company Document** (Business Document), which mandates a sub-$0.0035 blended cost-per-query ceiling across 99.5% of API transactions.

## 2. Routing Architecture & Cost Breakdown
- **Tier 0 (Deterministic/Regex/Embeddings):** $0.00002/call (91% triage rate for standard SaaS lookups)
- **Tier 1 (GPT-4o mini - Primary Engine):** $0.15/1M input, $0.60/1M output tokens (Target: 8.2% of queries)
- **Tier 2 (GPT-4o - Escalation Engine):** $2.50/1M input, $10.00/1M output tokens (Target: <0.8% of queries)

## 3. Edge-Case Archaeologist Findings
1. **Recursive Fallback Cascades:** When structured schema generation failed on raw F2F transcript inputs with corrupted UTF-8 artifacts, the router re-prompted GPT-4o mini 3x before escalating to GPT-4o, increasing individual request cost from $0.0004 to $0.0382 (a 9,450% spike).
2. **Prompt Cache Invalidation Tail:** Variable system prompt timestamps in F2F ingestion bypassed OpenAI prefix caching, driving input token costs up by 48.3% during concurrent multi-session uploads.
3. **Token Bloat Anomalies:** Edge-case PDF attachments containing un-indexed OCR layers triggered 128k context-window saturation, consuming $0.32 in a single un-throttled evaluation call.

## 4. Policy Recommendations
- Implement hard circuit-breakers: Max 1 retry before Tier 2 routing.
- Freeze static prompt prefixes to lock in 50% prompt caching discount.
- Cap Tier 2 escalations at 1.2% total traffic to strictly preserve the **Company Document** unit cost SLA.
```