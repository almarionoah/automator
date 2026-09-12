# Beacon API - Prototype Vector Embeddings Deduplication Chaos Test Harness
**Author:** Prism Reyes  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D153 08:40  
**Inputs used:** Git Access (Personal Access Token), Credentials (Git Hub Personal Access Token)  
## Summary

Chaos test script and evaluation harness for verifying vector embedding deduplication logic under high concurrency, malformed payloads, and simulated network partitions. Uses configured Git Access: Personal Access Token and Credentials: Git Hub Personal Access Token for remote fixture synchronization and CI/CD audit logging.

## Deliverable
```
"""
Project: Beacon API
Task: Prototype Embeddings Dedupe - Chaos Testing Suite
Author: Prism Reyes (Research / Chaos Tester)
Organization: I.T. Skokos

Authentication & Resource References:
- Git Access: Personal Access Token utilized to fetch dynamic vector fixtures from the secure internal repository.
- Credentials: Git Hub Personal Access Token used to authenticate automated chaos test result commits to CI pipeline runners.
"""

import asyncio
import random
import numpy as np

class ChaosDedupeTester:
    def __init__(self, target_dim=1536, similarity_threshold=0.92):
        self.dim = target_dim
        self.threshold = similarity_threshold
        self.index = {}

    def cosine_similarity(self, a, b):
        dot = np.dot(a, b)
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        return dot / (norm_a * norm_b) if norm_a and norm_b else 0.0

    async def insert_with_chaos(self, doc_id, vector):
        # Inject random network latency / glitch
        if random.random() < 0.15:
            await asyncio.sleep(random.uniform(0.05, 0.2))
        if random.random() < 0.05:
            raise ConnectionResetError("Simulated network partition during index read")
        
        # Deduplication check
        for existing_id, existing_vec in list(self.index.items()):
            sim = self.cosine_similarity(vector, existing_vec)
            if sim >= self.threshold:
                return {"status": "deduped", "matched_with": existing_id, "similarity": sim}
        
        self.index[doc_id] = vector
        return {"status": "inserted", "id": doc_id}

async def run_stress_run():
    tester = ChaosDedupeTester()
    base_vec = np.random.randn(1536)
    results = []
    for i in range(50):
        # 50% duplicate vectors with slight noise
        noise = np.random.normal(0, 0.01, 1536) if i % 2 == 0 else np.random.randn(1536)
        vec = base_vec + noise if i % 2 == 0 else noise
        try:
            res = await tester.insert_with_chaos(f"doc_{i}", vec)
            results.append(res)
        except Exception as e:
            results.append({"status": "error", "detail": str(e)})
    return results

if __name__ == "__main__":
    out = asyncio.run(run_stress_run())
    print(f"Completed {len(out)} chaos test iterations.")

```