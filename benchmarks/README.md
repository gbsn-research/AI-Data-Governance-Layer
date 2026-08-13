# Benchmark Method — Public Toolkit 0.5.3

The published core benchmark files in `benchmarks/results/` are the **Toolkit 0.5.0 paper-evaluation baseline** and are retained unchanged for reproducibility. The benchmark code remains runnable under Toolkit 0.5.3. The separate pipeline microbenchmark is regenerated for the current toolkit.

The core benchmark measures the **reference ADGL governance engine only**. It excludes retrieval, connector I/O, network communication, model inference, token generation, external persistence, human-review latency, and execution of external consequential actions.

Published baseline workloads use:
- 3 warm-up runs per workload;
- 20 measured runs for ordinary workloads and 12 for the largest 5,000-object / 150-rule workloads;
- a fresh Python process for each core-engine workload;
- object scaling at 10 actual policy rules;
- rule scaling at 1,000 candidate objects;
- a 0-rule baseline to separate fixed engine/validation/audit cost from additional rule-processing cost.

Machine-readable core results include mean, standard deviation, median, p95, quartiles, IQR, minimum, and maximum. The paper uses **median and IQR as the primary descriptive statistics**; this is an initial reference-artifact baseline, not a production tail-latency study.

Run the published core baseline with:

```bash
PYTHONPATH=. python benchmarks/benchmark.py --iterations 20
python benchmarks/plot_results.py
```

The benchmark runner emits environment metadata, including Python version, platform, CPU model, logical CPU count, memory, toolkit/specification version, timestamp, and Git commit where available.

A separate warmed single-process pipeline microbenchmark exercises `INFORM`, `DECIDE`, and `ACT` governance decisions over the same 1,000-object fixture and stops before external human workflow or API execution:

```bash
PYTHONPATH=. python benchmarks/pipeline_benchmark.py
```
