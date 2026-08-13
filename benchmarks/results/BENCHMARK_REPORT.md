# Benchmark Report — Paper-Evaluated Toolkit 0.5.0 Baseline

The current public toolkit is **0.5.3**; these historical core-engine measurements are retained because they are the values reported by the v0.9 paper.

These measurements are a reproducible baseline for the unoptimized Python reference runtime. They report the actual rule counts used by the harness and include a zero-rule baseline.

- Toolkit version: `0.5.0`
- Specification version: `0.3.0`
- Python: `3.13.5`
- Platform: `Linux-6.18.35-x86_64-with-glibc2.41`
- Logical CPU count: `5`
- CPU: `AMD EPYC 9V74 80-Core Processor`
- Timestamp (UTC): `2026-08-12T16:37:58.280814+00:00`

## Method

- Warmup runs per workload: 3
- Default measured runs: 20
- Largest-workload measured runs: 12
- Isolation: each workload executed in a fresh Python subprocess
- Scope: governance engine only; excludes retrieval, network, model inference, token generation, connector I/O and external persistence
- Primary publication statistics: median and interquartile range (IQR).

| Dimension | Objects | Rules | Runs | Median ms | IQR ms | Mean ms | Std. dev. ms |
|---|---:|---:|---:|---:|---:|---:|---:|
| objects | 10 | 10 | 20 | 0.603 | 0.019 | 0.615 | 0.031 |
| objects | 100 | 10 | 20 | 4.789 | 0.162 | 4.852 | 0.257 |
| objects | 1000 | 10 | 20 | 48.353 | 2.315 | 54.779 | 27.569 |
| objects | 5000 | 10 | 12 | 227.293 | 12.032 | 246.640 | 39.006 |
| rules | 1000 | 0 | 20 | 36.100 | 0.853 | 41.567 | 24.522 |
| rules | 1000 | 5 | 20 | 42.463 | 1.790 | 48.850 | 23.691 |
| rules | 1000 | 25 | 20 | 64.852 | 2.605 | 67.651 | 7.500 |
| rules | 1000 | 100 | 20 | 155.753 | 31.224 | 178.999 | 43.491 |
| rules | 1000 | 150 | 12 | 218.541 | 93.796 | 258.000 | 49.877 |

## Interpretation

Median evaluation cost rises with both candidate-object count and rule count. The zero-rule workload shows that structured copying, runtime validation, disposition bookkeeping, and audit construction impose a fixed cost before additional rule evaluation. The largest workloads show wider variability, so these values are reference-artifact baselines rather than production throughput claims.

The benchmark excludes retrieval, network calls, connector I/O, foundation-model inference, token generation, external persistence, human-review latency, and execution of real consequential actions.
