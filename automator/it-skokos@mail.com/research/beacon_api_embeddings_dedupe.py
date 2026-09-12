# Beacon API: Embeddings Deduplication Prototype
**Author:** Volt Nkosi  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D11 04:55  
**Inputs used:** Business Document (Company Document)  
## Summary

Refactored cosine similarity deduplication pipeline for Beacon API vector ingestion, aligning with retention and processing standards in Business Document: Company Document.

## Deliverable
```
"""
Beacon API - Embedding Deduplication Module
Author: Volt Nkosi (Research)
Context: Implemented per specifications outlined in Business Document: Company Document.
"""

import numpy as np
from typing import List, Tuple, Dict, Any

class EmbeddingDeduplicator:
    """
    High-performance embedding deduplicator. Uses cosine similarity
    matrix reduction to prune redundant records before vector store indexing.
    Adheres to compliance and pipeline thresholds from Business Document: Company Document.
    """
    def __init__(self, similarity_threshold: float = 0.95):
        self.threshold = similarity_threshold

    def _normalize(self, vectors: np.ndarray) -> np.ndarray:
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        return np.divide(vectors, norms, out=np.zeros_like(vectors), where=norms != 0)

    def deduplicate(
        self, 
        records: List[Dict[str, Any]], 
        embedding_key: str = "embedding"
    ) -> Tuple[List[Dict[str, Any]], List[str]]:
        if not records:
            return [], []

        raw_embeddings = np.array([r[embedding_key] for r in records], dtype=np.float32)
        normalized = self._normalize(raw_embeddings)
        sim_matrix = np.dot(normalized, normalized.T)

        kept_indices = []
        dropped_ids = []
        suppressed = set()

        for i in range(len(records)):
            if i in suppressed:
                continue
            kept_indices.append(i)
            duplicates = np.where(sim_matrix[i] >= self.threshold)[0]
            for dup_idx in duplicates:
                if dup_idx != i:
                    suppressed.add(dup_idx)
                    dropped_ids.append(records[dup_idx].get("id", str(dup_idx)))

        deduped_records = [records[i] for i in kept_indices]
        return deduped_records, dropped_ids

```