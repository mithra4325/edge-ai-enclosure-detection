# M2.4: Standardized Fair Benchmarking Report

**Student Name:** Mithra Ravi  
**Milestone:** M2 Optimize  
**Task:** Fair benchmark (Max marks: 4)  
**Proof Statement:** *"I run 20 warm-up and 100+ timed runs at batch 1. I show median and p95 latency, FPS and model size"*

---

## 1. Benchmarking Methodology

To ensure scientifically valid and repeatable latency figures, this benchmark followed rigorous edge benchmarking standards:

1. **Dedicated Warm-Up:** **20 warm-up iterations** executed prior to recording timings to allow instruction cache population, JIT kernel caching, and thread-pool initialization.
2. **Sample Size:** **100 consecutive timed runs** executed at strictly **Batch Size 1**.
3. **High-Resolution Clock:** Monitored via Python `time.perf_counter()` on the physical Broadcom BCM2712 SoC.
4. **Outlier Resistance:** Median ($50^{\text{th}}$ percentile) latency is reported to resist background OS scheduling spikes, accompanied by the $95^{\text{th}}$ percentile ($p95$) tail latency.
5. **Active Thermal Monitoring:** Measured under sustained load with Raspberry Pi 5 Active Cooler enabled.

---

## 2. Benchmark Comparison Table

| Model Architecture & Format | Model File Size | Median Latency (ms) | P95 Latency (ms) | Throughput (FPS) | Relative Speedup vs PyTorch |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **PyTorch FP32 Baseline (`best.pt`)** | **5.16 MB** | **468.2 ms** | **695.2 ms** | **2.14 FPS** | $1.00\times$ (Baseline) |
| **ONNX FP32 (`best.onnx`)** | **9.34 MB** | **256.8 ms** | **393.4 ms** | **3.89 FPS** | **$1.82\times$ Faster** |
| **ONNX INT8 Quantized (`best_int8.onnx`)** | **2.72 MB** | **274.6 ms** | **445.8 ms** | **3.64 FPS** | **$1.71\times$ Faster** |

---

## 3. Engineering Insights & Latency Distribution

1. **ONNX Runtime Acceleration ($1.82\times$):**
   - ONNX Runtime's native `CPUExecutionProvider` out-performs standard PyTorch CPU on ARM64 by **$82\%$** (reducing median latency from 468.2ms down to 256.8ms). This is due to operator fusion and kernel vectorization tailored for ARMv8.2-A NEON cores.
2. **P95 Latency Reduction:**
   - The tail latency drops significantly from 695.2ms in PyTorch to **393.4ms** in ONNX, delivering substantially smoother frame delivery without stuttering.
3. **Model Footprint Optimization:**
   - The quantized INT8 model slashes disk footprint from 9.34 MB to **2.72 MB** (a **$70.9\%$** savings) while maintaining high FPS (3.64 FPS) on raw CPU.
4. **Raw Data:** All 100 runs are archived in [`fair_benchmark_data.csv`](fair_benchmark_data.csv).
