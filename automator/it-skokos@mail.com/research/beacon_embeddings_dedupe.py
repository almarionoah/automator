# Beacon API - Cost-Optimized Embeddings Deduplication Prototype
**Author:** Vex Reyes  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D17 18:05  
**Inputs used:** Business Document (Company Document)  
## Summary

Implementation script for deduplicating high-dimensional text embeddings to minimize downstream vector storage and LLM inference costs, aligned with data governance rules from Business Document: Company Document.

## Deliverable
```
"""
Beacon API - Embeddings Deduplication Prototype
Author: Vex Reyes (Research - Cost Optimization Focus)
Project: Beacon API
Reference: Business Document: Company Document (used to enforce data retention limits and similarity thresholds)
"""

import numpy as np
from typing import List, Dict, Tuple

class EmbeddingsDeduplicator:
    def __init__(self, similarity_threshold: float = 0.96):
        # Threshold derived from constraints outlined in Business Document: Company Document
        self.threshold = similarity_threshold
        self.index: List[np.ndarray] = []
        self.metadata_store: Dict[int, dict] = {}

    def _cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return float(np.dot(a, b) / (norm_a * norm_b))

    def deduplicate_and_index(self, records: List[Tuple[dict, np.ndarray]]) -> Dict[str, int]:
        saved_vectors = 0
        deduped_vectors = 0

        for meta, vec in records:
            is_duplicate = False
            for existing_idx, existing_vec in enumerate(self.index):
                sim = self._cosine_similarity(vec, existing_vec)
                if sim >= self.threshold:
                    is_duplicate = True
                    # Link alias to existing cluster to save storage
                    self.metadata_store[existing_idx].setdefault("aliases", []).append(meta.get("id"))
                    deduped_vectors += 1
                    break
            
            if not is_duplicate:
                new_idx = len(self.index)
                self.index.append(vec)
                self.metadata_store[new_idx] = {"primary_id": meta.get("id"), "aliases": []}
                saved_vectors += 1

        return {
            "retained_embeddings": saved_vectors,
            "eliminated_duplicates": deduped_vectors,
            "storage_reduction_pct": round((deduped_vectors / max(1, len(records))) * 100, 2)
        }

```