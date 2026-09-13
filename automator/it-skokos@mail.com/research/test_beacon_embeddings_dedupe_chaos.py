# Beacon API Embeddings Deduplication Chaos Test Harness & Prototype
**Author:** Prism Marlow  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D16 23:50  
**Inputs used:** Business Document (Company Document)  
## Summary

Chaos test harness and prototype script evaluating vector deduplication under noise and edge conditions for the Beacon API, aligned with operational boundaries in Company Document.

## Deliverable
```
# Beacon API - Embeddings Deduplication Prototype & Chaos Suite
# Author: Prism Marlow (Research / Chaos Testing)
# Reference: Aligned with operational threshold standards defined in 'Company Document'.

import numpy as np
import random

class ChaosDedupeEngine:
    def __init__(self, similarity_threshold=0.92):
        # Baseline similarity threshold derived from specifications in Company Document
        self.threshold = similarity_threshold
        self.vector_index = {}

    def compute_similarity(self, v1: np.ndarray, v2: np.ndarray) -> float:
        norm1, norm2 = np.linalg.norm(v1), np.linalg.norm(v2)
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return float(np.dot(v1, v2) / (norm1 * norm2))

    def insert_or_dedupe(self, doc_id: str, embedding: np.ndarray) -> tuple[bool, str]:
        # Chaos injection: Random vector perturbation
        perturbed_vec = embedding.copy()
        if random.random() < 0.15:
            perturbed_vec += np.random.normal(0, 0.05, size=embedding.shape)

        for existing_id, existing_vec in self.vector_index.items():
            sim = self.compute_similarity(perturbed_vec, existing_vec)
            if sim >= self.threshold:
                return True, existing_id  # Deduplicated
        
        self.vector_index[doc_id] = embedding
        return False, doc_id

def run_chaos_test():
    engine = ChaosDedupeEngine(similarity_threshold=0.90)
    dim = 256
    base_vector = np.random.randn(dim)
    
    # Test dedupe match under synthetic drift
    engine.insert_or_dedupe("doc_orig", base_vector)
    duplicate_vector = base_vector + np.random.normal(0, 0.01, size=dim)
    is_dup, match_id = engine.insert_or_dedupe("doc_variant", duplicate_vector)
    
    print(f"Chaos Dedupe Run Complete. Deduped: {is_dup}, Matched ID: {match_id}")

if __name__ == '__main__':
    run_chaos_test()
```