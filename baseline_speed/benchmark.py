#!/usr/bin/env python3
"""
M1.3: Baseline Speed Benchmark Script
Measures actual inference latency, FPS, CPU load, RAM usage, and temperature
on Raspberry Pi 5 using the original trained YOLO Nano PyTorch weights.

Author: Mithra Ravi
Milestone: M1 Detect
"""

import sys
import time
import csv
from pathlib import Path
import psutil
import cv2
import numpy as np
from ultralytics import YOLO

def get_cpu_temp() -> float:
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            return round(float(f.read().strip()) / 1000.0, 1)
    except Exception:
        return 0.0

def run_baseline_benchmark(model_path: str = "models/best.pt", runs: int = 50, output_csv: str = "baseline_speed/baseline_results.csv"):
    weights = Path(model_path).resolve()
    if not weights.exists():
        raise FileNotFoundError(f"Model not found at: {weights}")

    print("=" * 70)
    print(" RASPBERRY PI 5 BASELINE PERFORMANCE BENCHMARK ")
    print("=" * 70)
    print(f"[*] Model:        {weights}")
    print(f"[*] Benchmark:    {runs} test iterations")
    print(f"[*] Device:       Raspberry Pi 5 Model B (ARM Cortex-A76 @ 2.4 GHz)")
    print("=" * 70)

    model = YOLO(str(weights))
    dummy_frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)

    # 1. Warm-up
    print("[*] Performing 5 warm-up iterations...")
    for _ in range(5):
        _ = model.predict(source=dummy_frame, conf=0.25, verbose=False)

    # 2. Benchmark Loop
    print(f"[*] Executing {runs} timed benchmark runs...")
    csv_path = Path(output_csv)
    csv_path.parent.mkdir(parents=True, exist_ok=True)

    records = []
    latencies = []

    for i in range(1, runs + 1):
        t0 = time.perf_counter()
        results = model.predict(source=dummy_frame, conf=0.25, verbose=False)
        lat_ms = (time.perf_counter() - t0) * 1000.0
        latencies.append(lat_ms)

        cpu_pct = round(psutil.cpu_percent(interval=None), 1)
        vm = psutil.virtual_memory()
        ram_mb = round(vm.used / (1024 * 1024), 1)
        temp_c = get_cpu_temp()
        fps = 1000.0 / max(lat_ms, 1e-4)

        records.append([
            time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            i,
            round(fps, 2),
            round(lat_ms, 2),
            cpu_pct,
            ram_mb,
            temp_c,
            len(results[0].boxes)
        ])
        time.sleep(0.05)

    with open(csv_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "frame_index", "fps", "inference_latency_ms", "cpu_usage_pct", "ram_usage_mb", "cpu_temp_c", "objects_detected"])
        writer.writerows(records)

    median_lat = float(np.median(latencies))
    mean_lat = float(np.mean(latencies))
    avg_fps = 1000.0 / median_lat

    print("\n" + "=" * 70)
    print(" BASELINE RESULTS SUMMARY ")
    print("=" * 70)
    print(f"  - Median Inference Latency: {median_lat:.1f} ms")
    print(f"  - Mean Inference Latency:   {mean_lat:.1f} ms")
    print(f"  - Measured FPS:             {avg_fps:.2f} FPS")
    print(f"  - Average CPU Load:         {np.mean([r[4] for r in records]):.1f}%")
    print(f"  - Average Temperature:      {np.mean([r[6] for r in records]):.1f}°C")
    print(f"  - Baseline CSV Saved to:    {csv_path}")
    print("=" * 70)

if __name__ == "__main__":
    run_baseline_benchmark()
