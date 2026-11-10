# Edge AI 3D-Printed Enclosure Detection: Milestone 1 Technical Report

**Project Title:** Real-Time Embedded Detection of 3D-Printed Sensor Enclosures  
**Author / Student:** Mithra Ravi (`mithra4325`)  
**Institution / Assessment:** Milestone 1 (M1 Detect — Edge AI Systems)  
**GitHub Repository:** [https://github.com/mithra4325/edge-ai-enclosure-detection](https://github.com/mithra4325/edge-ai-enclosure-detection)  
**Date of Milestone Completion:** November 10, 2026  

---

## Executive Summary

This report documents the design, dataset curation, model training, embedded deployment, live demonstration, and empirical evaluation of an Edge AI computer vision system deployed on a **Raspberry Pi 5 Single Board Computer (SBC)**. 

The primary task is real-time detection of a custom **3D-printed PIR sensor camera enclosure** using an embedded **YOLO Nano (`yolo26n`)** convolutional neural network coupled with a **Logitech C270 USB webcam**. All work was conducted using authentic physical hardware and the original Roboflow-trained model weights. 

The system achieves **100.0% mAP@0.5** on the held-out validation set and operates at an average inference latency of **454.5 ms** ($\approx 1.8\text{ – }3.4\text{ FPS}$) running purely on the 64-bit ARM Cortex-A76 CPU using ARM NEON vector SIMD instructions. An empirical evaluation also uncovered a key limitation: the model exhibits false-positive detections on non-enclosure white surfaces due to background bias in the v1 training set, establishing a clear technical baseline and roadmap for Milestone 2 (M2) optimization.

---

## 1. Problem Definition & Objectives

Modern edge computing and smart monitoring applications frequently require automated optical verification of mechanical enclosures, sensor packages, and IoT hardware installations. Conventional object detection models trained on standard datasets (e.g., COCO, Pascal VOC) contain generic classes such as "cup" or "person," but have no capability to recognize custom-fabricated mechanical housings.

The objectives of Milestone 1 were:
1. **Target Object Fabrication:** Design and 3D-print a custom sensor enclosure using CAD modeling.
2. **Dataset Creation:** Capture physical photographs under varied perspectives and tightly annotate them in Roboflow.
3. **Partition Integrity:** Implement a strict **70% / 20% / 10%** split ratio and cryptographically verify zero data leakage.
4. **Model Training:** Train an edge-appropriate YOLO Nano object detector and evaluate formal metrics (mAP@0.5, precision, recall).
5. **Physical Embedded Deployment:** Deploy the unquantized model onto a Raspberry Pi 5 without retraining or weight substitution.
6. **Live OpenCV Pipeline:** Build a robust, low-latency live camera streaming and inference pipeline with a telemetry HUD overlay.
7. **Empirical Benchmarking:** Quantify real-world CPU latency, application throughput (FPS), thermals, and memory utilization.
8. **Failure Mode Analysis:** Rigorously document model limitations and false-positive vulnerabilities discovered during live testing.

---

## 2. Target Object & CAD Modeling

The physical detection target is a custom PIR sensor enclosure:
- **CAD File:** [`cad/pir_sensor_enclosure_mithra_ravi.stl`](../cad/pir_sensor_enclosure_mithra_ravi.stl)
- **Material:** Polylactic Acid (PLA) 3D-printer filament.
- **Color:** White / light ivory with matte surface texture.
- **Physical Features:** Circular central lens aperture, rectangular mounting chassis, dual exterior screw tabs, cable passthrough cutout.

---

## 3. Dataset Preparation & Roboflow Workflow

The dataset was curated, annotated, and exported using the Roboflow computer vision platform:

- **Roboflow Workspace:** `mithu-1vntk`
- **Roboflow Project ID:** `object-detection-n6b60` (`enclosure detector`)
- **Dataset Version:** Version 1 (`2026-11-10 2:37pm`)
- **License:** Creative Commons Attribution 4.0 International (CC BY 4.0)
- **Total Images:** 40 authentic high-resolution photographs.
- **Total Labeled Instances:** 60 bounding box annotations.
- **Target Class:** `enclosure` (Single-class detection, ID `0`).
- **Partition Distribution:**
  - **Training Split:** 28 images (70.0%), 44 bounding boxes.
  - **Validation Split:** 8 images (20.0%), 11 bounding boxes.
  - **Held-Out Test Split:** 4 images (10.0%), 5 bounding boxes.
- **Cryptographic Leakage Audit:** SHA-256 hash digests verified 0 filename overlaps and 0 binary content collisions across all splits (confirmed by [`correct_split/verify_split.py`](../correct_split/verify_split.py)).
- **Preprocessing:** Auto-orientation applied (EXIF rotation normalization). Zero synthetic augmentations applied to preserve authentic physical measurements.

---

## 4. Model Architecture & Training Results

The model employs the Ultralytics **YOLO Nano (`yolo26n`)** architecture:
- **Architecture Family:** Decoupled anchor-free convolutional object detection head with PANet feature pyramid.
- **Parameters:** 2,504,190 (2.5 Million).
- **Computational Complexity:** 5.9 GFLOPs.
- **Input Resolution:** $640 \times 640$ auto-letterboxed pixels.
- **Layers:** 260 total convolutional and normalization layers.
- **Training Epochs:** 218 epochs (early-stop converged).
- **Weights Preserved:** [`models/best.pt`](../models/best.pt) (5.2 MB PyTorch) and [`models/best.onnx`](../models/best.onnx) (9.4 MB ONNX).

### Quantitative Metrics Summary

| Dataset Partition | Metric | Measured Value | Analysis / Meaning |
| :--- | :--- | :---: | :--- |
| **Roboflow Validation (8 imgs)** | **mAP @ 0.50** | **100.0%** | Perfect spatial bounding-box alignment at 50% IoU |
| **Roboflow Validation (8 imgs)** | **mAP @ 0.50:0.95** | **96.37%** | High geometric overlap across tight IoU sweeps |
| **Roboflow Validation (8 imgs)** | **Precision** | **100.0%** | Zero false detections on held-out validation set |
| **Roboflow Validation (8 imgs)** | **Recall** | **100.0%** | 100% of ground-truth validation enclosures localized |
| **Roboflow Validation (8 imgs)** | **Optimal F1-Score**| **1.00** | Achieved at confidence threshold $0.22$ |
| **Held-Out Test Split (4 imgs)**| **Test mAP @ 0.50** | **100.0%** | All 5 test targets localized ($93.0\%$ to $95.4\%$ conf) |
| **Physical Live Testing** | **Empirical Performance**| **Observed Sensitivity**| Detects enclosure reliably; exhibits white-surface false positives |

---

## 5. Raspberry Pi 5 Embedded Deployment

The complete application was deployed onto a physical **Raspberry Pi 5 Model B Rev 1.1**:

```text
Raspberry Pi 5 (BCM2712 Quad Cortex-A76 @ 2.4 GHz, 4GB RAM)
               │
               ├── Linux V4L2 Subsystem (/dev/video0)
               │     └── Logitech C270 USB Webcam (640x480 @ 30 FPS)
               │
               ├── Python 3.13.5 Virtual Environment (--system-site-packages)
               │     ├── Debian native OpenCV 4.10.0 (V4L2 hardware capture)
               │     ├── Debian native NumPy 2.2.4
               │     └── PyTorch 2.15.0+cpu (ARM NEON SIMD vector arithmetic)
               │
               ├── Application Modules
               │     ├── src/camera.py (Threaded non-blocking buffer stream)
               │     ├── src/detector.py (YOLO Nano inference & HUD overlay)
               │     └── src/monitor.py (Hardware telemetry & CSV logging)
               │
               └── Output Interfaces
                     ├── Live GUI Window (OpenCV on DISPLAY=:0)
                     └── Telemetry Logger (evidence/benchmark/baseline_results.csv)
```

---

## 6. Live Demonstration & Verification

Physical demonstration evidence was captured and archived in [`evidence/M1/06_live_demonstration/`](../evidence/M1/06_live_demonstration/):
1. **Live Video ([`live_demo_video.mov`](../evidence/M1/06_live_demonstration/live_demo_video.mov)):** High-speed capture ($2160 \times 3840$, 120 FPS) showing dynamic tracking and responsive camera frame acquisition.
2. **Screenshot 1 ([`live_demo_screenshot_1.png`](../evidence/M1/06_live_demonstration/live_demo_screenshot_1.png)):** Shows true enclosure detection at **76.1%** confidence with telemetry overlay.
3. **Screenshot 2 ([`live_demo_screenshot_2.png`](../evidence/M1/06_live_demonstration/live_demo_screenshot_2.png)):** Shows alternate oblique angle tracking at **74.5%** and **66.7%** confidence.

---

## 7. Baseline Performance & Telemetry Results

Benchmark data recorded in [`evidence/benchmark/baseline_results.csv`](../evidence/benchmark/baseline_results.csv):

| Metric | Measured Baseline Value | Context / Hardware Mode |
| :--- | :---: | :--- |
| **Inference Latency** | **454.5 ms** (range: 335 ms – 776 ms) | CPU-only PyTorch FP32 forward pass |
| **End-to-End Application FPS** | **1.83 – 3.35 FPS** | Includes capture, letterbox, forward pass, overlay, display |
| **Raw Camera Capture Speed** | **16.62 FPS** | Unthreaded V4L2 sequential frame read |
| **CPU Utilization** | **74.0% – 77.6%** | Multi-threaded PyTorch execution across 4 cores |
| **System RAM Usage** | **2,858 MB – 2,907 MB** | Includes OS, desktop session, and model tensors |
| **CPU Temperature** | **50.1°C – 51.2°C** | Raspberry Pi Active Cooler running dynamically |
| **GPU Utilization** | **0% (CPU Only)** | No GPU acceleration used (Raspberry Pi VideoCore VII lacks CUDA) |

---

## 8. Failure Analysis: The White-Surface False-Positive Problem

During real-world deployment, an important limitation was discovered: **the model frequently detects non-enclosure white surfaces (white paper, light desk edges, pale walls) as enclosures.**

### Working Hypotheses:
1. **Background Correlation:** In Dataset v1, all 40 photographs were captured on a dark brown wooden workbench. The model learned that any high-contrast white shape on a dark surface was an enclosure.
2. **Zero Hard Negatives:** Dataset v1 contained 0 images without enclosures. The loss function was never penalized for activating on white non-enclosure objects.

### Proposed M2 Mitigations:
1. Capture 60+ new images across white desks, metal tables, concrete, and varied rooms.
2. Inject 20+ hard-negative images (white paper, white boxes, non-enclosure plastic) labeled with zero boxes.
3. Train an improved v2 model and evaluate both v1 and v2 on the same untouched benchmark.

---

## 9. Conclusion & Milestone 2 Roadmap

Milestone 1 successfully established:
- A verified, authentic dataset and zero-leakage partition split.
- Successful embedded deployment of the original YOLO Nano model on Raspberry Pi 5.
- A functional, low-latency OpenCV live detection pipeline.
- Rigorous baseline benchmarking and empirical identification of failure modes.

Milestone 2 will focus on:
1. **Quantization & Acceleration:** Exporting to INT8 TFLite / ONNX Runtime to exceed 15+ FPS.
2. **Dataset v2 Expansion:** Injecting hard negatives to eliminate white-surface false positives.
3. **Fair Benchmarking:** Formally comparing FP32 vs INT8 accuracy and latency.
