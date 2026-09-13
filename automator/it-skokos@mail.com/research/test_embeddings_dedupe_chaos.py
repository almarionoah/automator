# Beacon API: Prototype Embeddings Deduplication Chaos Test Suite
**Author:** Zed Nkosi  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D16 06:25  
**Inputs used:** Business Document (Company Document)  
## Summary

Chaos test harness and resilience benchmark for the Beacon API vector deduplication prototype, validating failure modes and boundary thresholds aligned with the Company Document.

## Deliverable
```
"""
Beacon API - Embeddings Deduplication Prototype Chaos Test Suite
Author: Zed Nkosi (Research / Chaos Tester, I.T. Skokos)

Resource Utilization Note:
- 'Company Document': Utilized to extract the baseline vector similarity acceptance criteria (cosine threshold >= 0.985) and standard SLA tolerance limits for ingestion latency under degraded vector states.
"""

import numpy as np
import pytest
from typing import List, Tuple

COSINE_THRESHOLD = 0.985  # Governed by Company Document specifications

def cosine_similarity(v1: np.ndarray, v2: np.ndarray) -> float:
    norm = np.linalg.norm(v1) * np.linalg.norm(v2)
    return float(np.dot(v1, v2) / norm) if norm != 0 else 0.0

class EmbeddingDedupeEngine:
    def __init__(self, threshold: float = COSINE_THRESHOLD):
        self.threshold = threshold
        self.index: List[np.ndarray] = []

    def ingest(self, vector: np.ndarray) -> Tuple[bool, int]:
        if np.isnan(vector).any() or np.isinf(vector).any():
            raise ValueError("Vector payload corrupted: NaN/Inf detected.")
        if np.linalg.norm(vector) == 0:
            raise ValueError("Zero-magnitude vector rejected.")
        
        for idx, existing in enumerate(self.index):
            if cosine_similarity(vector, existing) >= self.threshold:
                return False, idx  # Identified duplicate
        self.index.append(vector)
        return True, len(self.index) - 1

# --- CHAOS & BOUNDARY TEST SCENARIOS ---

def test_adversarial_boundary_jitter():
    """Inject micro-perturbations around 0.985 threshold defined in Company Document."""
    engine = EmbeddingDedupeEngine()
    base = np.random.randn(1536)
    base /= np.linalg.norm(base)
    engine.ingest(base)

    for scale in [1e-4, 5e-4, 1e-2]:
        noisy = base + np.random.normal(0, scale, size=base.shape)
        noisy /= np.linalg.norm(noisy)
        sim = cosine_similarity(base, noisy)
        accepted, match_id = engine.ingest(noisy)
        if sim >= COSINE_THRESHOLD:
            assert not accepted, f"False negative: duplicate missed at sim={sim}"
        else:
            assert accepted, f"False positive: distinct vector dropped at sim={sim}"

def test_payload_corruption_handling():
    """Validate dedupe engine stability against degenerate inputs."""
    engine = EmbeddingDedupeEngine()
    with pytest.raises(ValueError, match="NaN/Inf"):
        engine.ingest(np.full(1536, np.nan))
    with pytest.raises(ValueError, match="Zero-magnitude"):
        engine.ingest(np.zeros(1536))

```