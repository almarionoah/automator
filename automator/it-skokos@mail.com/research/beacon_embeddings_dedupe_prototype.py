# Beacon API: Prototype Vector Embedding Deduplication Engine & Edge-Case Evaluation Harness
**Author:** Prism Ito  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D19 05:40  
**Inputs used:** Business Document (Company Document)  
## Summary

Prototype deduplication engine and edge-case test suite for Beacon API vector payloads, incorporating threshold calibration sourced from Company Document.

## Deliverable
```
"""
Project: Beacon API
Author: Prism Ito (Research - Edge-Case Archaeologist)
Task: prototype embeddings dedupe

Resource Reference:
- Business Document: 'Company Document' was reviewed to extract standardized semantic similarity thresholds (Section 4.2) and compliance deduplication criteria for blending I.T. Skokos SaaS platform telemetries with Face-to-Face service interaction embeddings.
"""

import numpy as np
from typing import List, Dict, Tuple, Set

COSINE_SIMILARITY_THRESHOLD = 0.942
NORM_EPSILON = 1e-12

class EmbeddingDeduplicator:
    def __init__(self, threshold: float = COSINE_SIMILARITY_THRESHOLD):
        self.threshold = threshold

    def deduplicate(self, records: List[Dict]) -> Tuple[List[Dict], List[Dict]]:
        unique_records: List[Dict] = []
        duplicate_records: List[Dict] = []
        seen_hashes: Set[int] = set()

        for rec in records:
            vec = np.array(rec["embedding"], dtype=np.float32)
            norm = np.linalg.norm(vec)
            
            # Edge Case 1: Degenerate vector norm (Zero-vector / padding anomaly)
            if norm < NORM_EPSILON or np.isnan(norm) or np.isinf(norm):
                rec["dedupe_flag"] = "MALFORMED_ZERO_OR_NON_FINITE_VECTOR"
                duplicate_records.append(rec)
                continue

            unit_vec = vec / norm
            byte_hash = hash(unit_vec.tobytes())
            
            # Edge Case 2: Bitwise duplicate
            if byte_hash in seen_hashes:
                rec["dedupe_flag"] = "EXACT_BITWISE_DUPLICATE"
                duplicate_records.append(rec)
                continue

            # Edge Case 3: Cosine proximity thresholding
            is_dupe = False
            for u_rec in unique_records:
                sim = float(np.dot(unit_vec, u_rec["_normalized_embedding"]))
                if sim >= self.threshold:
                    rec["dedupe_flag"] = f"SEMANTIC_COLLISION_SIM_{sim:.5f}"
                    rec["matched_id"] = u_rec["id"]
                    duplicate_records.append(rec)
                    is_dupe = True
                    break

            if not is_dupe:
                rec["_normalized_embedding"] = unit_vec
                seen_hashes.add(byte_hash)
                unique_records.append(rec)

        return unique_records, duplicate_records

if __name__ == "__main__":
    # Test harness simulating hybrid SaaS & F2F payloads per Company Document specs
    sample_batch = [
        {"id": "rec_001", "embedding": [0.1, 0.2, 0.3], "source": "SaaS_API"},
        {"id": "rec_002", "embedding": [0.10001, 0.20001, 0.30001], "source": "F2F_Transcript"},
        {"id": "rec_003", "embedding": [0.0, 0.0, 0.0], "source": "Corrupt_Stream"},
        {"id": "rec_004", "embedding": [0.8, -0.2, 0.1], "source": "SaaS_API"},
    ]
    deduper = EmbeddingDeduplicator()
    uniques, dupes = deduper.deduplicate(sample_batch)
    print(f"Retained: {len(uniques)}, Deduplicated: {len(dupes)}")
```