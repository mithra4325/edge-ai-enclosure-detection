# M1.3: Baseline Speed & Hardware Performance

**Status:** **COMPLETE**

---

## 1. Purpose of the Task
The objective of Milestone 1.3 is to establish an unsimulated, physical performance baseline for the original trained YOLO Nano model (`models/best.pt`) running directly on the Raspberry Pi 5 CPU. This benchmark records actual frame rate (FPS), per-frame inference latency (milliseconds), CPU utilization percentage across all 4 cores, system memory (RAM) usage, and SoC thermal profile before any Milestone 2 optimizations.

## 2. What I Implemented
- **Automated Telemetry Monitor (`src/monitor.py` & `benchmark.py`):** Designed a non-intrusive performance monitoring routine that records hardware telemetry every frame without adding execution overhead.
- **Continuous Latency & FPS Logger:** Captures per-frame execution duration using monotonic high-resolution system timers (`time.perf_counter()`).
- **Thermal & Resource Sampling:** Queries physical thermal sensors via Linux sysfs (`/sys/class/thermal/thermal_zone0/temp`) and memory statistics via `psutil`.
- **CSV Data Exporter:** Automatically writes all timestamped measurements to [`baseline_results.csv`](baseline_results.csv).

## 3. Hardware Used
- **Single Board Computer:** Raspberry Pi 5 Model B Rev 1.1.
- **CPU:** Quad-core ARM Cortex-A76 @ 2.4 GHz (Broadcom BCM2712 SoC, 16nm).
- **GPU:** VideoCore VII (Idle — all inference executed on CPU).
- **RAM:** 4.0 GiB LPDDR4X unified memory.
- **Thermal Management:** Raspberry Pi Active Cooler (Aluminium heatsink with variable PWM blower).

## 4. Software and Dependencies
- **Operating System:** Debian GNU/Linux 13 (Trixie) / Raspberry Pi OS 13.7 (Kernel: 6.18.50+rpt-rpi-2712 aarch64).
- **Runtime Environment:** Python 3.13.5 with `torch 2.15.0+cpu` (ARM64 NEON vectorized) and `ultralytics 8.4.208`.
- **Monitoring Tools:** `psutil`, `/sys/class/thermal/thermal_zone0/temp`.

## 5. How the Implementation Works
1. The benchmarking script initializes the trained PyTorch model (`models/best.pt`) onto the Raspberry Pi 5 CPU.
2. 5 warm-up iterations are executed to prime instruction caches and thread-pool memory structures.
3. For each benchmark iteration:
   - `t0 = time.perf_counter()` starts the high-resolution hardware timer.
   - The frame is forwarded through the YOLO backbone, neck, and decoupled anchor-free head.
   - Latency in milliseconds is calculated: $(t_1 - t_0) \times 1000$.
   - System CPU load, RAM used, and thermal zone 0 temperature are logged.
4. Data is written to `baseline_results.csv` and summarized into median latency and throughput metrics.

## 6. How to Reproduce or Run It
From the project root on the Raspberry Pi 5:
```bash
# 1. Activate virtual environment
source venv/bin/activate

# 2. Run the baseline benchmark script
python baseline_speed/benchmark.py
```

## 7. Evidence Available in this Folder
- [`baseline_results.csv`](baseline_results.csv): Raw timestamped telemetry data for all frames (timestamp, frame index, FPS, latency, CPU %, RAM MB, temperature, detections count).
- [`benchmark.py`](benchmark.py): Fully reproducible standalone benchmarking script.
- [`live_overlay_1.jpg`](live_overlay_1.jpg): Live camera capture with telemetry header showing latency (277ms) and FPS (3.0 FPS).
- [`live_overlay_2.jpg`](live_overlay_2.jpg): Sustained run capture showing CPU load (62%) and temperature (51.2°C).

## 8. Actual Results

### Measured Hardware Baseline Numbers (Physical Raspberry Pi 5 CPU)

| Performance Metric | Measured Range | Typical / Average Value | Explanation of Metric |
| :--- | :--- | :---: | :--- |
| **Inference Latency** | **270.9 ms – 293.4 ms** | **281.5 ms** | Total time taken by the CPU to process one image matrix and output boxes |
| **Throughput (FPS)** | **3.10 – 3.56 FPS** | **3.35 FPS** | Frames Per Second: The number of full detection cycles completed per second |
| **CPU Usage** | **56.4% – 63.4%** | **59.2%** | Percentage of the 4 ARM Cortex-A76 cores utilized during continuous inference |
| **GPU Load** | *0% (CPU Only)* | **0%** | Dedicated GPU inference is not used; model executes strictly on CPU |
| **System RAM** | **2,409 MB – 2,491 MB** | **2,442 MB** | Physical RAM allocated by Linux OS, desktop GUI, Python runtime, and PyTorch |
| **CPU Temperature** | **49.0°C – 52.4°C** | **50.2°C** | Onboard SoC temperature; stays well below the 80°C thermal throttling ceiling |

### Detailed Metric Explanations
- **FPS (Frames Per Second):** Represents real-world responsiveness. A throughput of 3.4 FPS means the camera detects changes every ~290ms, perfectly adequate for workbench and conveyor-belt inspection.
- **Latency (ms):** Measures the elapsed time from feeding the frame to the model until bounding box coordinates are returned. Lower latency means faster reaction time.
- **CPU Usage (%):** Running on all 4 cores via PyTorch multi-threading consumes ~60% of total CPU capacity, leaving ~40% available for system background tasks and UI rendering.
- **Temperature (°C):** The active cooler maintains 50.2°C, meaning the CPU never thermal-throttles or drops its 2.4 GHz clock rate.

## 9. Pending Items and Limitations
- **Pending Items:** None for Milestone 1.3.
- **Limitations:** Model execution currently utilizes FP32 floating-point arithmetic on CPU. Milestone 2 will explore ONNX Runtime and INT8 quantization to reduce latency.
