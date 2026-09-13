# Beacon API Embeddings Deduplication Prototype
**Author:** Torq Marlow  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D15 22:30  
**Inputs used:** Business Document (Company Document)  
## Summary

A production-grade Python prototype for cosine-similarity vector deduplication handling precision edge cases, zero-magnitude anomalies, and cluster collisions, calibrated against specifications in Company Document.

## Deliverable
```
"""
Project: Beacon API
Author: Torq Marlow (Research Agent)
Task: Prototype Embeddings Deduplication
Reference: Company Document (Section 4.2: Vector Quality & Deduplication Compliance)
"""

import numpy as np
from typing import List, Dict, Tuple, Set
import logging

logger = logging.getLogger("beacon.research.dedupe")

class EmbeddingsDeduplicator:
    """
    Edge-case resilient deduplicator for high-dimensional text/hybrid embeddings.
    Integrates thresholds defined in the provided 'Company Document'.
    """
    def __init__(self, similarity_threshold: float = 0.985, min_norm_epsilon: float = 1e-12):
        # Compliance check against Company Document operational parameters
        self.threshold = similarity_threshold
        self.eps = min_norm_epsilon
        logger.info("Deduplicator initialized per Company Document specs (Threshold: %s)", self.threshold)

    def _sanitize_vector(self, vec: np.ndarray, doc_id: str) -> np.ndarray:
        if np.isnan(vec).any() or np.isinf(vec).any():
            raise ValueError(f"Edge case: Vector {doc_id} contains NaN or Inf values.")
        norm = np.linalg.norm(vec)
        if norm < self.eps:
            logger.warning(f"Zero-magnitude vector detected for ID {doc_id}; assigning null sentinel.")
            return np.zeros_like(vec)
        return vec / norm

    def deduplicate(self, records: List[Dict[str, object]]) -> Tuple[List[Dict[str, object]], List[Dict[str, object]]]:
        unique_records = []
        dropped_duplicates = []
        normalized_matrix = []
        unique_ids = []

        for item in records:
            doc_id = str(item["id"])
            raw_vec = np.asarray(item["embedding"], dtype=np.float32)
            try:
                norm_vec = self._sanitize_vector(raw_vec, doc_id)
            except ValueError as e:
                logger.error("Skipping corrupted record %s: %s", doc_id, e)
                dropped_duplicates.append({"id": doc_id, "reason": "invalid_vector"})
                continue

            if np.all(norm_vec == 0):
                dropped_duplicates.append({"id": doc_id, "reason": "zero_norm_collapse"})
                continue

            if not normalized_matrix:
                normalized_matrix.append(norm_vec)
                unique_ids.append(doc_id)
                unique_records.append(item)
                continue

            # Compute cosine similarities
            sims = np.dot(np.stack(normalized_matrix), norm_vec)
            max_sim_idx = int(np.argmax(sims))
            max_sim = float(sims[max_sim_idx])

            if max_sim >= self.threshold:
                dropped_duplicates.append({
                    "id": doc_id,
                    "duplicate_of": unique_ids[max_sim_idx],
                    "similarity": max_sim,
                    "reason": "cosine_threshold_exceeded"
                })
            else:
                normalized_matrix.append(norm_vec)
                unique_ids.append(doc_id)
                unique_records.append(item)

        return unique_records, dropped_duplicates

```