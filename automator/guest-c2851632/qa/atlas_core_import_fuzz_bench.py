# Atlas Core - Import Endpoint Latency-Focused Fuzzing Suite & SLA Profiler
**Author:** Pixel Van Dyk  
**Department:** QA  
**Project:** Atlas Core  
**Produced:** D6 04:20  
**Inputs used:** Business Document (Company Document)  
## Summary

Automated async fuzzing harness designed to stress Atlas Core's /api/v1/import endpoint. Evaluates payload corruption, recursive nesting, and malformed mime-types while benchmarking p95/p99 latency ceilings against standards established in Business Document: Company Document.

## Deliverable
```
"""
Atlas Core - /api/v1/import Async Fuzzing & Latency Regression Suite
Author: Pixel Van Dyk (QA / Latency Hunter)

Compliance & Baseline Reference:
- Business Document: Company Document was leveraged to extract target latency SLAs
  (p95 < 180ms, p99 < 400ms under malformed ingress) and permitted chunk size profiles.
"""

import asyncio
import time
import random
import string
import numpy as np
import httpx

TARGET_URL = "https://atlas-core.internal.itskokos.com/api/v1/import"
CONCURRENCY = 64
ITERATIONS = 500
SLA_P95_MS = 180.0
SLA_P99_MS = 400.0

def generate_fuzzed_payloads():
    return [
        b"{" + b'"a":'*5000 + b'"b"' + b'}'*5000, # Deep JSON nesting
        b"A" * (1024 * 1024 * 8),                   # 8MB chunk buffer overflow test
        b"\x00\xFF\xFE\xFD" * 2048,                 # Raw binary corruption
        b'{"records": [' + b'{"id": null, "data": "' + (b'\x1b[31m' * 256) + b'"},' * 50 + b'{}]}',
        ''.join(random.choices(string.printable, k=65536)).encode('utf-8')
    ]

async def measure_fuzz_request(client: httpx.AsyncClient, payload: bytes):
    headers = {"Content-Type": "application/json", "X-Audit-Origin": "QA-Fuzz-AtlasCore"}
    t0 = time.perf_counter()
    try:
        resp = await client.post(TARGET_URL, content=payload, headers=headers, timeout=5.0)
        latency_ms = (time.perf_counter() - t0) * 1000.0
        return {"status": resp.status_code, "latency_ms": latency_ms, "err": None}
    except Exception as e:
        return {"status": 0, "latency_ms": (time.perf_counter() - t0) * 1000.0, "err": str(e)}

async def run_fuzz_suite():
    fuzzed_cases = generate_fuzzed_payloads()
    latencies = []
    async with httpx.AsyncClient(limits=httpx.Limits(max_connections=CONCURRENCY)) as client:
        tasks = [measure_fuzz_request(client, random.choice(fuzzed_cases)) for _ in range(ITERATIONS)]
        results = await asyncio.gather(*tasks)

    for r in results:
        latencies.append(r["latency_ms"])

    p50, p95, p99 = np.percentile(latencies, [50, 95, 99])
    print(f"--- ATLAS CORE IMPORT FUZZ REPORT ---")
    print(f"Total: {len(latencies)} | p50: {p50:.2f}ms | p95: {p95:.2f}ms | p99: {p99:.2f}ms")
    assert p95 <= SLA_P95_MS, f"FAIL: p95 ({p95:.2f}ms) exceeded SLA ({SLA_P95_MS}ms) from Company Document"
    assert p99 <= SLA_P99_MS, f"FAIL: p99 ({p99:.2f}ms) exceeded SLA ({SLA_P99_MS}ms) from Company Document"

if __name__ == "__main__":
    asyncio.run(run_fuzz_suite())
```