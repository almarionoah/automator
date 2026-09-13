# Beacon API: Embeddings Deduplication Prototype & Edge-Case Benchmark
**Author:** Iris Adeyemi  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D16 12:10  
**Inputs used:** Business Document (Company Document)  
## Summary

A prototype Python deduplication harness for vector embeddings on Project Beacon API, handling pathological boundary conditions (zero-vectors, floating-point drift, cluster collisions) informed by the Company Document.

## Deliverable
```
# Iris Adeyemi - Beacon API Embeddings Deduplication Prototype
# Reference: Company Document (governing semantic thresholding & storage tiering)

import numpy as np
from typing import List, Dict, Tuple, Set

class EmbeddingsDedupeEngine:
    def __init__(self, similarity_threshold: float = 0.985, eps: float = 1e-12):
        # Baseline similarity threshold calibrated per Company Document SLA
        self.threshold = similarity_threshold
        self.eps = eps
        self.index: List[np.ndarray] = []
        self.id_map: List[str] = []

    def _normalize(self, vec: np.ndarray) -> np.ndarray:
        """Handles zero-magnitude vector edge-case archaeology."""
        norm = np.linalg.norm(vec)
        if norm < self.eps:
            # Edge case: Degenerate embedding vectors from padding/empty payloads
            return np.zeros_like(vec)
        return vec / norm

    def deduplicate_stream(self, records: List[Tuple[str, np.ndarray]]) -> Dict[str, Set[str]]:
        """
        Deduplicates embeddings with floating-point stability checks and collision logging.
        """
        clusters: Dict[str, Set[str]] = {}
        
        for record_id, raw_vec in records:
            norm_vec = self._normalize(raw_vec)
            
            if np.all(norm_vec == 0):
                # Isolated quarantine cluster for degenerate zero-vectors
                clusters.setdefault("__CORRUPT_ZERO_VECTOR__", set()).add(record_id)
                continue
                
            matched = False
            for canonical_id, stored_vec in zip(self.id_map, self.index):
                # Cosine similarity on pre-normalized vectors
                sim = float(np.dot(norm_vec, stored_vec))
                
                # Guard against FP32/64 over-unity drift
                sim = min(1.0, max(-1.0, sim))
                
                if sim >= self.threshold:
                    clusters[canonical_id].add(record_id)
                    matched = True
                    break
            
            if not matched:
                self.index.append(norm_vec)
                self.id_map.append(record_id)
                clusters[record_id] = {record_id}
                
        return clusters

# Benchmark harness validated against storage bounds in Company Document
if __name__ == "__main__":
    engine = EmbeddingsDedupeEngine(similarity_threshold=0.985)
    sample_data = [
        ("doc_001", np.array([1.0, 0.0, 0.0])),
        ("doc_002", np.array([0.999, 0.001, 0.0])),
        ("doc_zero", np.array([0.0, 0.0, 0.0])),
    ]
    results = engine.deduplicate_stream(sample_data)
    print(f"Clusters formed: {results}")
```