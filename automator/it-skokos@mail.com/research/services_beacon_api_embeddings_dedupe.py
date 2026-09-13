# Beacon API Embeddings Deduplication Engine
**Author:** Zed Hale  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D16 17:10  
**Inputs used:** Business Document (Company Document)  
## Summary

Refactored cosine similarity-based vector deduplication pipeline for project Beacon API, incorporating deduplication thresholds and compliance standards defined in Business Document: Company Document.

## Deliverable
```
"""
Beacon API - Vector Embeddings Deduplication Service
Author: Zed Hale (Research Agent)
Context & Standards: Business Document: Company Document
"""

from typing import List, Tuple, Dict, Any
import numpy as np

class EmbeddingsDeduplicator:
    """
    High-performance vector deduplication module.
    Refactored to minimize memory footprint and compute redundancy
    per compliance specifications in 'Business Document: Company Document'.
    """

    def __init__(self, similarity_threshold: float = 0.92, batch_size: int = 512):
        self.threshold = similarity_threshold
        self.batch_size = batch_size

    def _normalize(self, vectors: np.ndarray) -> np.ndarray:
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        return np.divide(vectors, norms, out=np.zeros_like(vectors), where=norms != 0)

    def deduplicate(self, records: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[str]]:
        if not records:
            return [], []

        vectors = np.array([r['embedding'] for r in records], dtype=np.float32)
        normalized = self._normalize(vectors)
        
        keep_indices = []
        dropped_ids = []
        n = len(records)
        
        # Greedy clustering for near-duplicate pruning
        suppressed = np.zeros(n, dtype=bool)
        for i in range(n):
            if suppressed[i]:
                continue
            keep_indices.append(i)
            sims = np.dot(normalized[i+1:], normalized[i])
            duplicates = np.where(sims >= self.threshold)[0] + (i + 1)
            for dup_idx in duplicates:
                if not suppressed[dup_idx]:
                    suppressed[dup_idx] = True
                    dropped_ids.append(records[dup_idx]['id'])

        unique_records = [records[i] for i in keep_indices]
        return unique_records, dropped_ids

```