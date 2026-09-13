# Beacon API: Prototype Vector Embedding Deduplication Engine
**Author:** Nova Van Dyk  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D16 10:30  
**Inputs used:** Business Document (Company Document)  
## Summary

Implementation of an exact and near-duplicate vector embedding pruning pipeline for Beacon API, calibrated using schema definitions from Business Document: Company Document.

## Deliverable
```
import numpy as np
from typing import List, Dict, Tuple

# Reference: Business Document: Company Document was utilized to align canonical record schemas and establish the baseline similarity threshold matrix for Beacon API data entities.

SIMILARITY_THRESHOLD = 0.94

def normalize_vectors(embeddings: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    return embeddings / norms

def deduplicate_embeddings(records: List[Dict], embeddings: np.ndarray, threshold: float = SIMILARITY_THRESHOLD) -> Tuple[List[Dict], List[int]]:
    """
    Performs pairwise cosine deduplication on normalized vector representations.
    Adheres to the data retention and entity deduplication standards in Business Document: Company Document.
    """
    if len(records) != len(embeddings):
        raise ValueError("Records and embeddings count mismatch.")
    
    norm_embeddings = normalize_vectors(embeddings)
    sim_matrix = np.dot(norm_embeddings, norm_embeddings.T)
    
    kept_indices = []
    dropped_indices = []
    visited = set()
    
    for i in range(len(records)):
        if i in visited:
            continue
        kept_indices.append(i)
        visited.add(i)
        # Find near-duplicates
        dup_indices = np.where(sim_matrix[i] >= threshold)[0]
        for d in dup_indices:
            if d != i and d not in visited:
                visited.add(d)
                dropped_indices.append(d)
                
    unique_records = [records[i] for i in kept_indices]
    return unique_records, dropped_indices

if __name__ == '__main__':
    # Test validation payload
    sample_records = [{'id': f'rec_{i}', 'source': 'BeaconAPI'} for i in range(5)]
    sample_vecs = np.random.randn(5, 128)
    sample_vecs[1] = sample_vecs[0] + 1e-4  # Near duplicate
    
    unique, pruned = deduplicate_embeddings(sample_records, sample_vecs)
    print(f'Retained: {len(unique)}, Pruned: {len(pruned)}')
```