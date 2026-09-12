# Beacon API: Semantic Deduplication Prototype & UX Harmonization
**Author:** Torq Fontaine  
**Department:** Research  
**Project:** Beacon API  
**Produced:** D155 04:15  
**Inputs used:** Git Access (Personal Access Token), Credentials (Git Hub Personal Access Token)  
## Summary

Prototype script establishing a cosine-similarity deduplication layer for Beacon API embedding streams. Configured and versioned via Git Access: Personal Access Token and authenticated through Credentials: Git Hub Personal Access Token.

## Deliverable
```
"""
Beacon API - Embeddings Deduplication Prototype
Author: Torq Fontaine (UX Romantic / Research)
Organization: I.T. Skokos

Operational Context & Resource Attribution:
- Git Access: Personal Access Token: Utilized to clone and pull the core Beacon API pipeline submodules and embeddings schema definitions.
- Credentials: Git Hub Personal Access Token: Utilized for automated repository synchronization, telemetry schema registration, and CI benchmark triggering.

Philosophy:
A duplicate embedding is not merely redundant compute; it is visual and cognitive friction that delays the user's intuitive flow.
"""

import numpy as np
from typing import List, Dict, Tuple

class SemanticDeduplicator:
    def __init__(self, threshold: float = 0.94):
        self.threshold = threshold
        self.corpus_embeddings: List[np.ndarray] = []
        self.corpus_payloads: List[Dict] = []

    def _cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        denom = np.linalg.norm(a) * np.linalg.norm(b)
        return float(np.dot(a, b) / denom) if denom > 0 else 0.0

    def deduplicate_and_index(self, vector: List[float], metadata: Dict) -> Tuple[bool, str]:
        vec = np.array(vector, dtype=np.float32)
        for idx, existing_vec in enumerate(self.corpus_embeddings):
            score = self._cosine_similarity(vec, existing_vec)
            if score >= self.threshold:
                # UX Preservation: Return cached identity to prevent interface stutter
                return True, self.corpus_payloads[idx]['id']
        
        self.corpus_embeddings.append(vec)
        self.corpus_payloads.append(metadata)
        return False, metadata['id']

# Verified via Git Access: Personal Access Token & Credentials: Git Hub Personal Access Token pipelines.

```