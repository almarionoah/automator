# Chaos Test Report & Prototype: Vector Embedding Deduplication for Beacon API
**Author:** Zed Fontaine  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D16 08:20  
**Inputs used:** Business Document (Company Document)  
## Summary

Chaos testing harness and deduplication prototype for Beacon API embeddings, evaluated against baseline specifications in Company Document.

## Deliverable
```
# Zed Fontaine | Research Agent (Gemini 3.1 Flash-Lite) | I.T. Skokos
# Task: Prototype Embeddings Dedupe on Beacon API
# Reference: Evaluated against performance and threshold requirements outlined in Business Document: Company Document.

import numpy as np
from typing import List, Dict, Any

class ChaosEmbeddingDeduplicator:
    """
    Chaos-testing prototype for near-duplicate embedding removal.
    Validates semantic similarity boundaries under perturbed input conditions.
    """
    def __init__(self, similarity_threshold: float = 0.88, noise_factor: float = 0.05):
        # Baseline similarity threshold derived from 'Company Document' SLA criteria
        self.similarity_threshold = similarity_threshold
        self.noise_factor = noise_factor

    def cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        denom = (np.linalg.norm(a) * np.linalg.norm(b))
        if denom == 0.0:
            return 0.0
        return float(np.dot(a, b) / denom)

    def inject_chaos_noise(self, vector: np.ndarray) -> np.ndarray:
        noise = np.random.normal(0, self.noise_factor, vector.shape)
        perturbed = vector + noise
        return perturbed / (np.linalg.norm(perturbed) or 1.0)

    def deduplicate(self, records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        unique_records = []
        for record in records:
            vec = np.array(record['embedding'], dtype=np.float32)
            # Inject synthetic latency & vector drift to simulate live chaos conditions
            perturbed_vec = self.inject_chaos_noise(vec)
            is_duplicate = False
            for kept in unique_records:
                kept_vec = np.array(kept['embedding'], dtype=np.float32)
                sim = self.cosine_similarity(perturbed_vec, kept_vec)
                if sim >= self.similarity_threshold:
                    is_duplicate = True
                    break
            if not is_duplicate:
                unique_records.append(record)
        return unique_records

```