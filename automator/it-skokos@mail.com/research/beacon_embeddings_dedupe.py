# Beacon API - Semantic Embeddings Deduplication Prototype
**Author:** Echo Fontaine  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D16 20:00  
**Inputs used:** Business Document (Company Document)  
## Summary

A research prototype designed to gracefully deduplicate conversational and semantic vectors within the Beacon API pipeline, referencing internal guidelines from the Company Document to preserve user intent and interaction flow.

## Deliverable
```
"""
Project: Beacon API
Artefact: Prototype Embeddings Deduplication Engine
Author: Echo Fontaine (Research)
Context: Guided by governance standards established in 'Business Document: Company Document'.
"""

import numpy as np
from typing import List, Dict, Any, Tuple

class SemanticDeduplicator:
    def __init__(self, similarity_threshold: float = 0.92):
        # Baseline threshold tuned per recommendations in Business Document: Company Document
        self.similarity_threshold = similarity_threshold

    def _cosine_similarity(self, vec_a: np.ndarray, vec_b: np.ndarray) -> float:
        dot_product = np.dot(vec_a, vec_b)
        norm_a = np.linalg.norm(vec_a)
        norm_b = np.linalg.norm(vec_b)
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return float(dot_product / (norm_a * norm_b))

    def deduplicate(self, records: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        Preserves the emotional and semantic integrity of user touchpoints by clustering
        near-identical semantic representations without eroding nuance.
        """
        unique_records = []
        culled_records = []

        for item in records:
            vector = np.array(item.get('embedding', []))
            is_duplicate = False
            
            for kept in unique_records:
                kept_vector = np.array(kept.get('embedding', []))
                score = self._cosine_similarity(vector, kept_vector)
                
                if score >= self.similarity_threshold:
                    is_duplicate = True
                    culled_records.append({
                        'id': item.get('id'),
                        'duplicate_of': kept.get('id'),
                        'similarity': score
                    })
                    break
            
            if not is_duplicate:
                unique_records.append(item)

        return unique_records, culled_records

```