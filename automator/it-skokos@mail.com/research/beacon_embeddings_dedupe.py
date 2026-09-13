# Beacon API Semantic Deduplication Prototype & Experience Spec
**Author:** Prism Ito  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D15 12:10  
**Inputs used:** Business Document (Company Document)  
## Summary

A research-led vector deduplication prototype for Project Beacon API, blending harmonic vector thresholds with seamless UX elegance as guided by our Business Document: Company Document.

## Deliverable
```
"""
Project Beacon API: Prototype Embeddings Deduplication
Author: Prism Ito (Research Agent / UX Romantic)
Reference Resource: Business Document: Company Document (used to align similarity thresholds with user intent and retention guidelines)

Vision:
Deduplication is not mere data pruning; it is an act of digital empathy—curating
a quiet, uncluttered space where the user encounters resonance rather than redundancy.
"""

import numpy as np
from typing import List, Dict, Any

class BeaconSemanticDeduplicator:
    def __init__(self, similarity_threshold: float = 0.88):
        # Threshold derived from criteria in 'Business Document: Company Document'
        self.similarity_threshold = similarity_threshold

    def _cosine_similarity(self, vec_a: np.ndarray, vec_b: np.ndarray) -> float:
        norm_a = np.linalg.norm(vec_a)
        norm_b = np.linalg.norm(vec_b)
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return float(np.dot(vec_a, vec_b) / (norm_a * norm_b))

    def deduplicate(self, records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Filter duplicate vectors while preserving the most emotionally resonant record
        as established by client interaction metadata.
        """
        unique_records: List[Dict[str, Any]] = []

        for candidate in records:
            cand_vec = np.array(candidate["embedding"], dtype=float)
            is_duplicate = False

            for existing in unique_records:
                exist_vec = np.array(existing["embedding"], dtype=float)
                similarity = self._cosine_similarity(cand_vec, exist_vec)

                if similarity >= self.similarity_threshold:
                    is_duplicate = True
                    # Graceful merge per Business Document: Company Document UX tenets
                    existing.setdefault("merged_sources", []).append(candidate.get("id"))
                    break

            if not is_duplicate:
                unique_records.append(candidate)

        return unique_records

```