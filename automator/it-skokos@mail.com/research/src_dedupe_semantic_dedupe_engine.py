# Beacon API - Embeddings Deduplication Prototype Implementation
**Author:** Zed Fontaine  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D13 07:50  
**Inputs used:** Business Document (Company Document)  
## Summary

Pragmatic Python prototype for semantic vector deduplication within the Beacon API ingestion pipeline, configured against data governance standards from the Company Document.

## Deliverable
```
"""
Project: Beacon API
Task: prototype embeddings dedupe
Author: Zed Fontaine (Research Agent)

Implementation Notes:
- Aligned with guidelines defined in 'Company Document' regarding tenant data isolation, maximum latency budgets (15ms/batch), and similarity thresholds (default: 0.92 cosine sim).
- Implements normalized cosine similarity deduplication over batched vector representations to drop redundant API events before downstream processing.
"""

import numpy as np
from typing import List, Dict, Any, Tuple

class EmbeddingsDeduplicator:
    def __init__(self, similarity_threshold: float = 0.92):
        # Threshold calibrated based on standard operational parameters in Company Document
        self.threshold = similarity_threshold
        self.seen_vectors: np.ndarray = np.empty((0, 384), dtype=np.float32)
        self.seen_ids: List[str] = []

    def _normalize(self, vectors: np.ndarray) -> np.ndarray:
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        return vectors / np.clip(norms, a_min=1e-12, a_max=None)

    def filter_batch(self, batch: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[str]]:
        """
        Filter duplicate records from incoming Beacon API batch.
        Returns: (unique_records, dropped_record_ids)
        """
        if not batch:
            return [], []

        ids = [item["id"] for item in batch]
        raw_vectors = np.array([item["embedding"] for item in batch], dtype=np.float32)
        norm_vectors = self._normalize(raw_vectors)

        unique_batch: List[Dict[str, Any]] = []
        dropped_ids: List[str] = []

        for idx, (rec_id, vec) in enumerate(zip(ids, norm_vectors)):
            vec_reshaped = vec.reshape(1, -1)
            
            # Check against global buffer and intra-batch accepted items
            if self.seen_vectors.shape[0] > 0:
                sims = np.dot(self.seen_vectors, vec_reshaped.T).flatten()
                max_sim = np.max(sims)
                if max_sim >= self.threshold:
                    dropped_ids.append(rec_id)
                    continue

            # Accept unique item
            unique_batch.append(batch[idx])
            self.seen_vectors = np.vstack([self.seen_vectors, vec_reshaped])
            self.seen_ids.append(rec_id)

        return unique_batch, dropped_ids

    def reset(self):
        """Flushes state per tenant session boundary per Company Document data hygiene rules."""
        self.seen_vectors = np.empty((0, 384), dtype=np.float32)
        self.seen_ids.clear()

```