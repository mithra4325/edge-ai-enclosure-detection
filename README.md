# Edge AI 3D-Printed Enclosure Detection

[![Model Architecture](https://img.shields.io/badge/Architecture-YOLO%20Nano%20(YOLO26n)-blue.svg)](https://github.com/ultralytics/ultralytics)
[![Roboflow](https://img.shields.io/badge/Roboflow-Trained%20v1-green.svg)](https://universe.roboflow.com/mithu-1vntk/object-detection-n6b60)
[![mAP@50](https://img.shields.io/badge/Validation%20mAP%4050-100%25-brightgreen.svg)]()
[![License](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

An end-to-end Edge AI object detection pipeline trained on **Roboflow** using a **YOLO Nano** (`yolo26n`) architecture to detect custom **3D-printed camera enclosures** in real time. 

This repository contains the trained model weights, portable ONNX export, dataset annotations, CAD models, and portable inference scripts ready to be deployed on desktop or edge devices (such as a Raspberry Pi).

---

## 1. Model & Training Overview

| Parameter | Specification | Details |
| :--- | :--- | :--- |
| **Model Type** | **YOLO Nano (`yolo26n`)** | Anchor-free decoupled head |
| **Parameters** | **2,504,190** (2.5M) | Lightweight edge-optimized backbone |
| **GFLOPs** | **5.9 GFLOPs** | Sub-millisecond desktop / low-latency edge inference |
| **Number of Layers** | 260 layers | Fused layers: 120 |
| **Input Resolution** | **640 &times; 640** | Auto-letterboxed |
| **Target Class** | `enclosure` | Single-class detector (ID: `0`) |
| **Training Epochs** | 218 epochs | Early-stop converged |
| **Validation mAP@50** | **100.0%** | Held-out validation split |
| **Validation mAP@50-95** | **96.37%** | Comprehensive IoU threshold sweep |
| **Precision / Recall** | **100.0% / 100.0%** | Optimal F1 at threshold `0.22` |
| **PyTorch Weights** | `models/best.pt` | Original trained weights (5.4 MB) |
| **ONNX Export** | `models/best.onnx` | Opset 17 portable export (9.3 MB) |

---

## 2. Repository Structure

```
edge-ai-enclosure-detection/
├── cad/
│   └── pir_sensor_enclosure_mithra_ravi.stl  # 3D-printed enclosure CAD model
├── data/
│   ├── data.yaml                             # Portable YOLO dataset manifest
│   ├── dataset_info.md                       # Full dataset split documentation
│   ├── samples/                              # Held-out sample images for instant verification
│   ├── train/                                # Training images and labels
│   ├── valid/                                # Validation images and labels
│   └── test/                                 # Test split images and labels
├── models/
│   ├── best.pt                               # Original trained YOLO Nano PyTorch weights
│   ├── best.onnx                             # Standalone ONNX runtime export
│   └── model_metadata.json                   # Comprehensive training and evaluation metrics
├── src/
│   ├── __init__.py
│   └── inference.py                          # Portable multi-backend inference engine
├── .gitignore                                # Strict secrets & temporary file filtering
├── requirements.txt                          # Cross-platform dependencies
└── README.md                                 # Project documentation
```

---

## 3. Quick Start: Clone & Run on Any Device

### Step 1: Clone the Repository
```bash
git clone https://github.com/mithra4325/edge-ai-enclosure-detection.git
cd edge-ai-enclosure-detection
```

### Step 2: Create a Virtual Environment and Install Dependencies
On Linux / macOS / Raspberry Pi OS:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

On Windows:
```cmd
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

## 4. Running Object Detection

### A. Run on Sample Images (PyTorch)
```bash
python src/inference.py --model models/best.pt --source data/samples/
```
The script will load the weights, run detection across all sample images, display detected bounding boxes with confidence scores, and save annotated outputs to `runs/detect/`.

### B. Run with Portable ONNX Model
```bash
python src/inference.py --model models/best.onnx --source data/samples/
```

### C. Run on a Live Camera / Webcam
Pass the camera index (e.g., `0` for default webcam, or `/dev/video0` on Linux):
```bash
python src/inference.py --model models/best.pt --source 0 --show
```
*Press `q` inside the video window to stop.*

### CLI Options Reference
| Argument | Default | Description |
| :--- | :--- | :--- |
| `--model` | `models/best.pt` | Path to `.pt` or `.onnx` model weights |
| `--source` | `data/samples` | Image path, folder of images, or camera index (`0`) |
| `--conf` | `0.25` | Confidence threshold ($0.0 - 1.0$) |
| `--iou` | `0.45` | Non-Maximum Suppression (NMS) IoU threshold |
| `--save-dir` | `runs/detect` | Output directory for saving annotated images |
| `--show` | `False` | Display live GUI window with detections |

---

## 5. Raspberry Pi 5 Deployment & Assessment Evidence (M1)

The trained model has been deployed and evaluated on physical **Raspberry Pi 5** hardware connected to a USB webcam.

### Hardware & Software Specifications
- **Device:** Raspberry Pi 5 Model B Rev 1.1 (4GB RAM)
- **Processor:** Broadcom BCM2712 Quad-core ARM Cortex-A76 @ 2.4 GHz (aarch64)
- **Operating System:** Debian GNU/Linux 13 (trixie) / Raspberry Pi OS 13.7 (Kernel 6.18.50+rpt-rpi-2712)
- **Python Version:** Python 3.13.5
- **Camera:** Logitech C270 HD USB Webcam (`/dev/video0`, UVC driver)
- **Inference Engine:** PyTorch CPU (`torch 2.15.0+cpu` & `ultralytics 8.4.208`) + OpenCV 4.10.0 + ONNX Runtime 1.31.1

---

### M1 Milestone Evidence Summary

#### M1.1 Camera & Repository Setup
- **USB Webcam Detection:** Successfully recognized Logitech C270 on `/dev/video0` with native 640x480 resolution at 30 FPS.
- **First Captured Frame:** Verified and saved at [`evidence/camera/test_frame.jpg`](evidence/camera/test_frame.jpg).
- **Repository Integrity:** Preserved original model weights (`models/best.pt`, `models/best.onnx`) without retraining.

#### M1.2 OpenCV Real-Time Pipeline
- **Modular Architecture:**
  - `src/camera.py`: Low-latency threaded capture pipeline eliminating frame queue buffer lag.
  - `src/detector.py`: Model loader, bounding box annotation, and high-contrast telemetry HUD.
  - `src/monitor.py`: Hardware statistics monitor (CPU %, RAM, Temperature) and CSV logger.
  - `src/inference.py`: Top-level CLI engine supporting both static evaluation and live camera streaming.
- **Live Detection Evidence:** Real-time detections with bounding boxes, confidence scores, and object counts saved at [`evidence/live_detection/`](evidence/live_detection/).
- **Offline Model Validation:** Sample image inferences with predicted bounding boxes saved at [`evidence/model_test/prediction.jpg`](evidence/model_test/prediction.jpg).

#### M1.3 Measured Baseline Speed & Telemetry
Actual hardware benchmarks recorded on the Raspberry Pi 5 CPU during live webcam detection:

| Metric | Measured Baseline Value | Assessment Status |
| :--- | :--- | :--- |
| **Inference Latency** | **270 ms – 290 ms** per frame | Measured via `time.perf_counter` |
| **Throughput (FPS)** | **3.3 – 3.5 FPS** (CPU inference) | Smooth real-time update |
| **CPU Usage** | **57% – 63%** across 4 cores | Stable execution |
| **RAM Usage** | **~2,450 MB** system total | < 65% of 4GB memory capacity |
| **CPU Operating Temp** | **49.0°C – 51.5°C** | Well below thermal throttling (80°C) |
| **Benchmark Log** | Saved with timestamps | [`evidence/benchmark/baseline_results.csv`](evidence/benchmark/baseline_results.csv) |

---

### Quick Launch on Raspberry Pi 5

To run the live detection application with a single command:
```bash
./run_detection.sh
```
*To exit live detection, press the **`q`** key in the OpenCV video window.*

To run in headless or benchmark mode:
```bash
./venv/bin/python src/inference.py --model models/best.pt --source 0 --max-frames 50
```

---

### Known Limitations & Future Optimizations
1. **CPU Execution:** Inference currently executes on the ARM Cortex-A76 CPU. Latency is ~280ms (3.5 FPS).
2. **Future Acceleration (M2 / M3):** Throughput can be accelerated further using ONNX Runtime with INT8 quantization, OpenVINO, or NPU acceleration if a Hailo-8L Raspberry Pi AI HAT is attached.

---

## 6. License & Acknowledgements

- **Author:** Mithra Ravi ([@mithra4325](https://github.com/mithra4325))
- **Dataset Hosting & Cloud Training:** [Roboflow Universe](https://universe.roboflow.com/mithu-1vntk/object-detection-n6b60) (CC BY 4.0)
- **Object Detection Framework:** [Ultralytics YOLO](https://github.com/ultralytics/ultralytics)
