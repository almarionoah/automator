# Chaos Validation & Prototype: Embeddings Deduplication Engine
**Author:** Jax Reyes  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D16 21:35  
**Inputs used:** Business Document (Company Document)  
## Summary

Prototype deduplication harness for Beacon API vector streams subjected to chaos injection, utilizing data classification and threshold policies established in Business Document: Company Document.

## Deliverable
```
"""
Project: Beacon API
Task: Prototype Embeddings Dedupe
Author: Jax Reyes (Research / Chaos Testing)

Resource Utilization:
- Business Document: Company Document was referenced to calibrate deduplication
  similarity thresholds (default 0.94 cosine similarity) and to enforce data retention
  and payload sanitation standards during edge-case simulations.
"""

import numpy as np
import random
import time
from typing import List, Dict, Any

class ChaosEmbeddingsDeduper:
    def __init__(self, threshold: float = 0.94, chaos_rate: float = 0.25):
        # Threshold aligned with Business Document: Company Document governance specs
        self.threshold = threshold
        self.chaos_rate = chaos_rate
        self.index: List[Dict[str, Any]] = []

    def _cosine_similarity(self, v1: np.ndarray, v2: np.ndarray) -> float:
        denom = (np.linalg.norm(v1) * np.linalg.norm(v2))
        return float(np.dot(v1, v2) / denom) if denom != 0 else 0.0

    def inject_chaos(self, vector: np.ndarray) -> np.ndarray:
        if random.random() < self.chaos_rate:
            fault = random.choice(["zero", "nan", "jitter", "spike"])
            if fault == "zero":
                return np.zeros_like(vector)
            elif fault == "nan":
                vec = vector.copy()
                vec[0] = np.nan
                return vec
            elif fault == "jitter":
                return vector + np.random.normal(0, 0.05, size=vector.shape)
            elif fault == "spike":
                return vector * 1000.0
        return vector

    def process_record(self, record_id: str, raw_vector: np.ndarray) -> Dict[str, Any]:
        vec = self.inject_chaos(raw_vector)
        
        # Resilience against invalid vectors
        if np.isnan(vec).any() or np.linalg.norm(vec) == 0:
            return {"id": record_id, "status": "REJECTED_CORRUPT", "duplicate_of": None}

        for item in self.index:
            sim = self._cosine_similarity(vec, item["vector"])
            if sim >= self.threshold:
                return {"id": record_id, "status": "DUPLICATE", "duplicate_of": item["id"], "similarity": sim}

        self.index.append({"id": record_id, "vector": vec})
        return {"id": record_id, "status": "INDEXED", "duplicate_of": None}

```