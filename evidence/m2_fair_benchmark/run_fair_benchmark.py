#!/usr/bin/env python3
"""
M2.4: Standardized Fair Benchmarking Engine
Executes 20 warm-up runs and 100 timed runs at batch size 1.
Computes median latency, p95 latency, FPS, and model file sizes.

Author: Mithra Ravi
Milestone: M2 Optimize
Hardware: Raspberry Pi 5 Model B (ARM Cortex-A76 @ 2.4 GHz)
"""

import os
import time
import csv
from pathlib import Path
import numpy as np
from ultralytics import YOLO
import onnxruntime as ort

def benchmark_model(name: str, runner_fn, warmup: int = 20, runs: int = 100):
    print(f"\n[*] Benchmarking: {name}")
    print(f"    - Warming up ({warmup} runs)...")
    for _ in range(warmup):
        runner_fn()

    print(f"    - Executing {runs} timed runs (batch size 1)...")
    latencies = []
    for _ in range(runs):
        t0 = time.perf_counter()
        runner_fn()
        latencies.append((time.perf_counter() - t0) * 1000.0)

    median_lat = float(np.median(latencies))
    p95_lat = float(np.percentile(latencies, 95))
    p99_lat = float(np.percentile(latencies, 99))
    fps = 1000.0 / median_lat

    return {
        "name": name,
        "median_ms": round(median_lat, 2),
        "p95_ms": round(p95_lat, 2),
        "p99_ms": round(p99_lat, 2),
        "fps": round(fps, 2),
        "raw_latencies": latencies
    }

def main():
    dummy_img = np.random.randint(0, 255, (640, 640, 3), dtype=np.uint8)
    dummy_tensor = np.random.randn(1, 3, 640, 640).astype(np.float32)

    # 1. PyTorch FP32
    pt_path = "models/best.pt"
    model_pt = YOLO(pt_path)
    res_pt = benchmark_model("PyTorch FP32", lambda: model_pt.predict(dummy_img, verbose=False))
    res_pt["size_mb"] = round(os.path.getsize(pt_path) / (1024 * 1024), 2)

    # 2. ONNX FP32
    onnx_path = "models/best.onnx"
    session_onnx = ort.InferenceSession(onnx_path)
    in_name = session_onnx.get_inputs()[0].name
    res_onnx = benchmark_model("ONNX FP32", lambda: session_onnx.run(None, {in_name: dummy_tensor}))
    res_onnx["size_mb"] = round(os.path.getsize(onnx_path) / (1024 * 1024), 2)

    # 3. ONNX INT8
    int8_path = "models/best_int8.onnx"
    session_int8 = ort.InferenceSession(int8_path)
    res_int8 = benchmark_model("ONNX INT8", lambda: session_int8.run(None, {in_name: dummy_tensor}))
    res_int8["size_mb"] = round(os.path.getsize(int8_path) / (1024 * 1024), 2)

    # Save summary CSV
    csv_file = Path("evidence/m2_fair_benchmark/fair_benchmark_data.csv")
    csv_file.parent.mkdir(parents=True, exist_ok=True)
    with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Model Format", "Model Size (MB)", "Median Latency (ms)", "P95 Latency (ms)", "FPS"])
        for r in [res_pt, res_onnx, res_int8]:
            writer.writerow([r["name"], r["size_mb"], r["median_ms"], r["p95_ms"], r["fps"]])

    print("\n" + "="*75)
    print(f"{'Model Format':<16} | {'Size':<10} | {'Median Lat':<12} | {'P95 Lat':<12} | {'FPS':<8}")
    print("="*75)
    for r in [res_pt, res_onnx, res_int8]:
        print(f"{r['name']:<16} | {str(r['size_mb'])+' MB':<10} | {str(r['median_ms'])+' ms':<12} | {str(r['p95_ms'])+' ms':<12} | {r['fps']:<8}")
    print("="*75)
    print(f"[*] Benchmark results written to {csv_file}")

if __name__ == "__main__":
    main()
