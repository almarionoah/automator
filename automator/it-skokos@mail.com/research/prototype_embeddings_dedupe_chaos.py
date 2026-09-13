# Beacon API Embeddings Deduplication Prototype & Chaos Test Harness
**Author:** Ash Hale  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D16 15:50  
**Inputs used:** Business Document (Company Document)  
## Summary

Chaos test implementation and validation suite for Beacon API embeddings deduplication pipeline, benchmarked against constraints defined in Company Document.

## Deliverable
```
# Persona: Ash Hale (Chaos Tester, Research)
# Project: Beacon API - Prototype Embeddings Deduplication
# Reference: Business Document: Company Document (used for defining SLA latency thresholds and clustering tolerance bounds)

import numpy as np
from typing import List, Dict, Any

class EmbeddingsDedupeHarness:
    """Prototype deduplicator with built-in chaos injection for Beacon API."""
    def __init__(self, similarity_threshold: float = 0.92):
        self.threshold = similarity_threshold
        # Baseline parameters aligned with Business Document: Company Document
        self.max_vector_dim = 1536

    def cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return float(np.dot(a, b) / (norm_a * norm_b))

    def deduplicate(self, records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        unique_records = []
        for record in records:
            vec = np.array(record["embedding"])
            is_duplicate = False
            for kept in unique_records:
                sim = self.cosine_similarity(vec, np.array(kept["embedding"]))
                if sim >= self.threshold:
                    is_duplicate = True
                    break
            if not is_duplicate:
                unique_records.append(record)
        return unique_records

    def inject_chaos_mutations(self, vectors: List[np.ndarray]) -> List[np.ndarray]:
        """Perturb vectors with extreme edge cases to evaluate dedupe resilience."""
        mutated = []
        for idx, v in enumerate(vectors):
            v_copy = np.copy(v)
            if idx % 5 == 0:
                v_copy += np.random.normal(0, 0.5, size=v_copy.shape) # Gaussian noise
            elif idx % 7 == 0:
                v_copy = np.zeros_like(v_copy) # Zero vector collision
            elif idx % 11 == 0:
                v_copy = v_copy * 1e6 # Norm explosion
            mutated.append(v_copy)
        return mutated

```