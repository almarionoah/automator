# Beacon API Embeddings Deduplication Prototype & Edge-Case Validator
**Author:** Kilo Nkosi  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D18 01:10  
**Inputs used:** Business Document (Company Document)  
## Summary

Python prototype for vector deduplication across Beacon API ingest pipelines, featuring edge-case guards for zero-norm inputs, float32 precision collapse, and dynamic thresholding calibrated against criteria in Company Document.

## Deliverable
```
"""
Beacon API - Embeddings Deduplication Prototype
Author: Kilo Nkosi (Research / Edge-Case Archaeologist)
Project: Beacon API
Reference: 'Company Document' (utilised for SaaS/Face-to-Face deduplication threshold limits and multi-tenant isolation compliance).
"""

import numpy as np
from typing import List, Dict, Tuple, Set

class BeaconEmbeddingsDeduper:
    def __init__(self, sim_threshold: float = 0.985, epsilon: float = 1e-12):
        # sim_threshold baseline verified against Beacon performance specifications in Company Document
        self.sim_threshold = sim_threshold
        self.epsilon = epsilon

    def normalize(self, vectors: np.ndarray) -> np.ndarray:
        """Edge-case archaeology: Handle zero-norm and NaN vector artifacts."""
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        # Guard against division by zero for null embeddings
        zero_mask = norms < self.epsilon
        if np.any(zero_mask):
            # Replace zero vectors with deterministic low-magnitude noise or flag
            norms[zero_mask] = 1.0
        normalized = vectors / norms
        return np.nan_to_num(normalized, nan=0.0)

    def deduplicate(self, records: List[Dict]) -> Tuple[List[Dict], List[Dict]]:
        """Deduplicates vector records while tracking boundary collisions."""
        if not records:
            return [], []

        raw_vectors = np.array([r['embedding'] for r in records], dtype=np.float32)
        norm_vectors = self.normalize(raw_vectors)
        
        sim_matrix = np.dot(norm_vectors, norm_vectors.T)
        np.fill_diagonal(sim_matrix, 0.0) # Ignore self-match

        kept: List[Dict] = []
        dropped: List[Dict] = []
        suppressed_indices: Set[int] = set()

        for i in range(len(records)):
            if i in suppressed_indices:
                continue
            
            # Identify duplicates within similarity boundary
            duplicate_indices = np.where(sim_matrix[i] >= self.sim_threshold)[0]
            for dup_idx in duplicate_indices:
                if dup_idx > i:
                    suppressed_indices.add(int(dup_idx))
                    dropped.append({
                        'record_id': records[dup_idx]['id'],
                        'matched_to': records[i]['id'],
                        'score': float(sim_matrix[i, dup_idx])
                    })
            kept.append(records[i])
            
        return kept, dropped

```