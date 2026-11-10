# Model Card: Custom 3D-Printed Enclosure Detector (YOLO26n)

**Model Architecture:** YOLO Nano (`yolo26n`)  
**Task:** Single-Class Object Detection  
**Target Class:** `enclosure` (Class ID `0`)  
**Author / Developer:** Mithra Ravi (`mithra4325`)  
**Deployment Platform:** Raspberry Pi 5 Model B (ARM Cortex-A76 @ 2.4 GHz)  
**Date:** November 10, 2026  

---

## 1. Model Overview

This model is a custom-trained **YOLO Nano (`yolo26n`)** convolutional object detector designed for real-time localization of custom 3D-printed PIR sensor enclosures. It is optimized for embedded edge inference on resource-constrained platforms such as the Raspberry Pi 5.

| Specification | Technical Detail |
| :--- | :--- |
| **Model Format (Primary)** | PyTorch Checkpoint (`models/best.pt`, 5.2 MB) |
| **Model Format (Export)** | Standalone ONNX Opset 17 (`models/best.onnx`, 9.4 MB) |
| **Backbone & Neck** | Lightweight CNN with decoupled anchor-free detection head |
| **Total Parameters** | 2,504,190 (2.50 Million) |
| **Computational Demand**| 5.9 GFLOPs |
| **Layer Depth** | 260 layers |
| **Input Image Resolution** | $640 \times 640$ pixels (auto-letterboxed) |
| **Normalization** | Pixel values scaled to $[0.0, 1.0]$, BGR to RGB color conversion |
| **Target Hardware Backend** | ARM Cortex-A76 CPU via ARM NEON SIMD vector arithmetic |

---

## 2. Training Data & Procedure

- **Training Framework:** Ultralytics YOLO v8.4.208 / PyTorch.
- **Dataset Source:** Roboflow Universe (`mithu-1vntk/object-detection-n6b60`, Version 1).
- **Training Epochs:** 218 epochs (converged with early stopping).
- **Batch Size:** Automated multi-scale batching on Roboflow cloud infrastructure.
- **Training Split:** 28 physical photographs (44 bounding boxes).
- **Validation Split:** 8 physical photographs (11 bounding boxes).
- **Held-Out Test Split:** 4 physical photographs (5 bounding boxes).
- **Synthetic Augmentations:** None in v1 (pure authentic physical captures).

---

## 3. Evaluation Metrics

### Validation Split Results (Roboflow Validation Split)

| Evaluation Metric | Measured Value | Standard Target | Assessment Evaluation |
| :--- | :---: | :---: | :--- |
| **mAP @ 0.50** | **100.0%** (1.00) | &ge; 85% | Perfect spatial bounding-box alignment |
| **mAP @ 0.50:0.95** | **96.37%** (0.9637)| &ge; 70% | High overlap across spatial IoU thresholds |
| **Precision** | **100.0%** (1.00) | &ge; 85% | Zero false-positive detections on validation split |
| **Recall** | **100.0%** (1.00) | &ge; 85% | Zero false-negative omissions |
| **Optimal F1-Score** | **1.00** | &ge; 85% | Optimal F1 at confidence threshold $0.22$ |

### Held-Out Test Split Results

- Evaluated using [`train_and_run_detector/evaluate_detector.py`](../train_and_run_detector/evaluate_detector.py) on Raspberry Pi 5.
- **Sample 1 (`IMG_9650`):** 1 enclosure detected (**93.9%** confidence).
- **Sample 2 (`IMG_9668`):** 2 enclosures detected (**95.3%** and **93.0%** confidence).
- **Sample 3 (`IMG_9681`):** 1 enclosure detected (**95.3%** confidence).
- **Sample 4 (`IMG_9684`):** 1 enclosure detected (**95.4%** confidence).

---

## 4. Difference Between PyTorch and ONNX Models

- **`models/best.pt` (PyTorch Checkpoint, 5.2 MB):**
  - Contains full PyTorch module definitions, optimizer state, and floating-point weights.
  - Used for standard Python inference with `ultralytics.YOLO`.
  - Executed on Raspberry Pi 5 CPU using PyTorch's native C++ ATen CPU backend with OpenMP multi-threading.
- **`models/best.onnx` (ONNX Export, 9.4 MB):**
  - Self-contained computational graph exported at ONNX Opset 17.
  - Decoupled from PyTorch internals; can be executed via `onnxruntime` on ARM64.
  - Serves as the intermediate representation (IR) required for Milestone 2 quantization (INT8).

---

## 5. Intended Use & Deployment Scope

- **Intended Use:** Automated visual detection, verification, and inventory counting of 3D-printed PIR sensor enclosures in assembly or lab environments.
- **Operating Distance:** Optimal between $0.3\text{ m}$ and $1.5\text{ m}$ from the Logitech C270 camera.
- **Operating Environment:** Stable indoor ambient illumination ($300\text{ – }800\text{ lux}$).

---

## 6. Known Limitations & Failure Modes

1. **White Surface False-Positive Sensitivity:**
   - *Observation:* Pale or white rectangular objects (white paper, light desk corners, laptops) frequently trigger false enclosure detections with confidence scores between $22\%$ and $48\%$.
   - *Root Cause:* Dataset v1 was captured on a single dark brown workbench. The network learned a spurious correlation between high-contrast white surfaces and enclosure presence.
2. **Extreme Distance & Macro Scale:**
   - At distances $>2.5\text{ m}$, the enclosure projects onto $<20\times 20$ pixels, dropping below the detection threshold.
   - At distances $<0.1\text{ m}$, parts of the enclosure extend beyond the frame boundary, causing bounding-box clipping.
3. **CPU Inference Latency:**
   - FP32 CPU execution yields $\approx 454\text{ ms}$ latency ($\approx 1.8\text{ – }3.4\text{ FPS}$), requiring INT8 quantization in M2 for fluid real-time operation.
