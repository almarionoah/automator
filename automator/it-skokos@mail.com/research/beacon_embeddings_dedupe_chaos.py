# Beacon API - Embeddings Deduplication Chaos Test Harness
**Author:** Lyra Adeyemi  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D16 12:15  
**Inputs used:** Business Document (Company Document)  
## Summary

Chaos evaluation harness and test report for the prototype vector embeddings deduplication pipeline on Beacon API, integrated with requirements from Company Document.

## Deliverable
```
# Beacon API: Embeddings Deduplication Chaos Harness
# Author: Lyra Adeyemi (Research / Chaos Testing)
# Reference: Company Document (Business Document - used for baseline deduplication SLA, payload schema constraints, and vector dimension guidelines)

import numpy as np
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('ChaosDedupe')

class ChaosEmbeddingsDedupeRunner:
    def __init__(self, sim_threshold=0.92, dim=1536):
        # Baseline thresholds aligned with Company Document specifications
        self.sim_threshold = sim_threshold
        self.dim = dim
        self.vector_store = {}

    def cosine_similarity(self, a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    def inject_vector_drift_and_noise(self, vec, noise_factor=0.08):
        """Inject gaussian noise and zero-masking to simulate edge-case semantic drift."""
        noise = np.random.normal(0, noise_factor, size=vec.shape)
        corrupted = vec + noise
        mask = np.random.binomial(1, 0.95, size=vec.shape) # 5% dropouts
        return corrupted * mask

    def dedupe_check(self, item_id, vector):
        for stored_id, stored_vec in self.vector_store.items():
            score = self.cosine_similarity(vector, stored_vec)
            if score >= self.sim_threshold:
                return True, stored_id, score
        self.vector_store[item_id] = vector
        return False, None, 0.0

    def run_chaos_suite(self, sample_size=100):
        logger.info('Executing chaos dedupe stress run against Beacon API...')
        base_vector = np.random.randn(self.dim)
        self.dedupe_check('base_001', base_vector)

        false_negatives, false_positives = 0, 0
        for i in range(sample_size):
            noisy = self.inject_vector_drift_and_noise(base_vector)
            is_dup, match_id, score = self.dedupe_check(f'sample_{i}', noisy)
            if not is_dup:
                false_negatives += 1
                
        logger.info(f'Completed run: {sample_size} noisy mutations. Threshold: {self.sim_threshold}. False negatives: {false_negatives}')
        return {'samples': sample_size, 'false_negatives': false_negatives}
```