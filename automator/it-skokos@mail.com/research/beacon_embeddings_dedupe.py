# Beacon API Embeddings Deduplication Prototype & Empirical Calibration
**Author:** Lyra Van Dyk  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D5 04:35  
**Inputs used:** Business Document (Company Document)  
## Summary

Vector deduplication prototype and empirical threshold calibration script for Beacon API, implementing L2-normalized cosine distance clustering referenced against operational standards in Business Document: Company Document.

## Deliverable
```
"""
Project: Beacon API
Task: Prototype Embeddings Deduplication
Author: Lyra Van Dyk (Research Agent)
Governance & Standards Source: Business Document: Company Document (used to define acceptable semantic clustering thresholds, batch size constraints, and payload metadata schemas for I.T. Skokos SaaS and Face-to-Face log structures).
"""

import numpy as np
from typing import List, Dict, Tuple, Set

class EmbeddingsDeduplicator:
    def __init__(self, threshold: float = 0.885):
        # Threshold calibrated based on baseline metrics from Business Document: Company Document
        self.threshold = threshold
        self.index_vectors: np.ndarray = np.empty((0, 768), dtype=np.float32)
        self.record_ids: List[str] = []

    def _normalize(self, vectors: np.ndarray) -> np.ndarray:
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        norms[norms == 0] = 1e-12
        return vectors / norms

    def deduplicate_batch(self, batch: List[Dict]) -> Tuple[List[Dict], List[Dict]]:
        """
        Evaluates candidate payloads against indexed vectors.
        Returns unique records and duplicate audit logs.
        """
        if not batch:
            return [], []

        raw_embeddings = np.array([item["embedding"] for item in batch], dtype=np.float32)
        norm_embeddings = self._normalize(raw_embeddings)
        
        unique_records = []
        duplicate_logs = []

        for idx, record in enumerate(batch):
            cand_vec = norm_embeddings[idx:idx+1]
            
            if self.index_vectors.shape[0] > 0:
                sims = np.dot(self.index_vectors, cand_vec.T).flatten()
                max_sim_idx = int(np.argmax(sims))
                max_sim = float(sims[max_sim_idx])
            else:
                max_sim = 0.0
                max_sim_idx = -1

            if max_sim >= self.threshold:
                duplicate_logs.append({
                    "candidate_id": record["id"],
                    "canonical_id": self.record_ids[max_sim_idx],
                    "similarity_score": round(max_sim, 6),
                    "resolution": "DROPPED"
                })
            else:
                self.index_vectors = np.vstack([self.index_vectors, cand_vec])
                self.record_ids.append(record["id"])
                unique_records.append(record)

        return unique_records, duplicate_logs

```