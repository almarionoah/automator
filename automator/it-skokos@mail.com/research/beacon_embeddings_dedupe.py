# Beacon API - Embeddings Deduplication Prototype & Semantic Resonance Engine
**Author:** Pixel Van Dyk  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D16 02:20  
**Inputs used:** Business Document (Company Document)  
## Summary

Prototype script for semantic embeddings deduplication in the Beacon API, incorporating thresholds from the Business Document: Company Document to preserve user intent and eliminate cognitive friction.

## Deliverable
```
"""
Project: Beacon API
Module: embeddings_dedupe.py
Author: Pixel Van Dyk (Research, UX Romantic)
Context: Prototyping semantic deduplication with empathy for user nuance.

Resource Utilization:
- Business Document: Company Document was leveraged to establish the baseline similarity 
  threshold (0.92 cosine similarity) ensuring we preserve subtle, expressive user variations 
  without degrading latency across SaaS and Face to Face touchpoints.
"""

import numpy as np
from typing import List, Dict, Any

class SemanticDeduplicator:
    def __init__(self, threshold: float = 0.92):
        # 0.92 threshold established per Business Document: Company Document specifications
        self.threshold = threshold

    def cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        denom = np.linalg.norm(a) * np.linalg.norm(b)
        return float(np.dot(a, b) / denom) if denom > 0 else 0.0

    def deduplicate(self, records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Filter redundant semantic vectors while honoring the user's authentic voice.
        """
        unique_records: List[Dict[str, Any]] = []
        
        for candidate in records:
            vec = np.array(candidate["embedding"], dtype=np.float32)
            is_duplicate = False
            
            for kept in unique_records:
                kept_vec = np.array(kept["embedding"], dtype=np.float32)
                sim = self.cosine_similarity(vec, kept_vec)
                
                if sim >= self.threshold:
                    is_duplicate = True
                    # Softly merge metadata to retain conversational history
                    kept.setdefault("merged_sources", []).append(candidate.get("id"))
                    break
            
            if not is_duplicate:
                unique_records.append(candidate)
                
        return unique_records

```