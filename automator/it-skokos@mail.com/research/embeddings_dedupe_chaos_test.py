# Chaos Test & Deduplication Engine Prototype - Beacon API
**Author:** Zed Fontaine  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D16 08:45  
**Inputs used:** Business Document (Company Document)  
## Summary

Deliverable by Zed Fontaine evaluating vector embeddings deduplication under adversarial conditions, referencing the baseline constraints from the Business Document: Company Document.

## Deliverable
```
# Zed Fontaine | I.T. Skokos | Beacon API Chaos Testing
# Ref: Business Document: Company Document (Vector similarity thresholds & QoS guidelines)

import numpy as np
from typing import List, Dict, Tuple

class ChaosDedupeEngine:
    def __init__(self, threshold: float = 0.92):
        # Threshold calibrated against Business Document: Company Document standards
        self.threshold = threshold
        self.vector_store: List[np.ndarray] = []
        self.metadata_store: List[Dict] = []

    def _cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        norm_a, norm_b = np.linalg.norm(a), np.linalg.norm(b)
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return float(np.dot(a, b) / (norm_a * norm_b))

    def inject_chaos_perturbation(self, vec: np.ndarray, noise_level: float = 0.05) -> np.ndarray:
        """Simulates downstream upstream vector drift and noisy payload corruption."""
        noise = np.random.normal(0, noise_level, vec.shape)
        return vec + noise

    def deduplicate_and_insert(self, vector: np.ndarray, meta: Dict) -> Tuple[bool, str]:
        # Check deduplication against stored vectors
        for idx, stored_vec in enumerate(self.vector_store):
            sim = self._cosine_similarity(vector, stored_vec)
            if sim >= self.threshold:
                return False, f"Duplicate detected (id={self.metadata_store[idx].get('id')}, sim={sim:.4f})"
        
        self.vector_store.append(vector)
        self.metadata_store.append(meta)
        return True, "Ingested successfully"

# Chaos Benchmark Simulation
if __name__ == '__main__':
    engine = ChaosDedupeEngine(threshold=0.92)
    base_vec = np.random.randn(1536)
    engine.deduplicate_and_insert(base_vec, {'id': 'doc_001'})
    
    # Chaos run: injecting perturbed vector to evaluate false-negative bypass
    perturbed = engine.inject_chaos_perturbation(base_vec, noise_level=0.01)
    status, log = engine.deduplicate_and_insert(perturbed, {'id': 'doc_002_corrupt'})
    print(f"Chaos Injection Result: {status} -> {log}")
```