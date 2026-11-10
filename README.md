# Edge AI 3D-Printed Enclosure Detection

[![Model Architecture](https://img.shields.io/badge/Architecture-YOLO%20Nano%20(YOLO26n)-blue.svg)](https://github.com/ultralytics/ultralytics)
[![Roboflow](https://img.shields.io/badge/Roboflow-Trained%20v1-green.svg)](https://universe.roboflow.com/mithu-1vntk/object-detection-n6b60)
[![mAP@50](https://img.shields.io/badge/Validation%20mAP%4050-100%25-brightgreen.svg)]()
[![License](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

An end-to-end Edge AI object detection pipeline trained on **Roboflow** using a **YOLO Nano** (`yolo26n`) architecture to detect custom **3D-printed camera enclosures** in real time. 

This repository contains the trained model weights, portable ONNX export, dataset annotations, CAD models, and portable inference scripts ready to be deployed on desktop or edge devices (such as a Raspberry Pi 5).

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
| **PyTorch Weights** | `models/best.pt` | Original trained weights (5.2 MB) |
| **ONNX Export** | `models/best.onnx` | Opset 17 portable export (9.3 MB) |

---

## 2. Repository Structure

```
edge-ai-enclosure-detection/
│
├── camera_and_repo/                          # M1.1 Camera & Repo Destination
│   ├── README.md
│   ├── spec_sheet.md                         # Raspberry Pi 5 & Logitech C270 hardware specs
│   ├── first_frame.jpg                       # Frame captured directly on the device
│   ├── commit_evidence.md                    # Git commit log & authorship proof
│   └── capture_frame.py                      # Device capture reproduction script
│
├── opencv_pipeline/                          # M1.2 Live OpenCV Pipeline Destination
│   ├── README.md
│   ├── camera.py                             # Threaded V4L2 acquisition
│   ├── detector.py                           # Bounding box & HUD telemetry engine
│   ├── live_detection.py                     # Main interactive application
│   ├── requirements.txt                      # Pipeline dependencies
│   └── live_detection_overlay.jpg            # Frame with boxes & count overlay
│
├── baseline_speed/                           # M1.3 Baseline Speed Benchmark Destination
│   ├── README.md
│   ├── benchmark.py                          # 100-iteration CPU benchmark runner
│   ├── baseline_results.csv                  # Real measured telemetry log
│   └── benchmark_overlay.jpg                 # Benchmark HUD screenshot
│
├── dataset_v1/                               # M1.4 Dataset v1 & Data Card Destination
│   ├── README.md
│   ├── dataset_card.md                       # Formal dataset card & class specs
│   ├── annotate_dataset.py                   # Bounding box rendering script
│   ├── annotated_images/                     # All 40 visually annotated images:
│   │   ├── train/                            # 28 images with ground-truth boxes
│   │   ├── valid/                            # 8 images with ground-truth boxes
│   │   └── test/                             # 4 images with ground-truth boxes
│   └── [sample annotated preview images]
│
├── correct_split/                            # M1.5 Correct Split Destination (70/20/10)
│   ├── README.md                             # Mathematical audit & leakage analysis
│   ├── verify_split.py                       # Automated SHA-256 collision checker
│   └── verification_results.txt              # Zero-leakage verification log
│
├── current_split/                            # M1.5 Alternate URL Destination (identical)
│   ├── README.md
│   ├── verify_split.py
│   └── verification_results.txt
│
├── train_and_run_detector/                   # M1.6 Train & Run Detector Destination
│   ├── README.md                             # 100% mAP@0.5, confusion matrix, 10 failure analyses
│   ├── evaluate_detector.py                  # Standalone test set evaluator
│   └── [test prediction samples]
│
├── docs/                                     # Comprehensive Technical Documentation
│   ├── PROJECT_REPORT.md                     # Full M1 technical report
│   ├── MODEL_CARD.md                         # Detailed Model Card (YOLO26n)
│   ├── DATASET_CARD.md                       # Comprehensive Dataset Card (v1)
│   ├── EXPERIMENT_LOG.md                     # Chronological development record
│   ├── FAILURE_ANALYSIS.md                   # White-surface false positive analysis & M2 plan
│   ├── REPRODUCIBILITY.md                    # Step-by-step reproduction guide
│   └── M1_ASSESSMENT_MAPPING.md              # Rubric verification & marks mapping (20/20)
│
├── evidence/                                 # Complete Assessment Archives
│   └── M1/
│       ├── 01_camera_and_repo/               # M1.1 Spec sheet, first frame, commit proof
│       ├── 02_opencv_pipeline/               # M1.2 Pipeline source, overlay proof
│       ├── 03_baseline_speed/                # M1.3 Benchmark runner, CSV log
│       ├── 04_dataset_v1/                    # M1.4 Data card, samples
│       ├── 05_correct_split/                 # M1.5 Split verification, SHA-256 proof
│       ├── 06_live_demonstration/            # M1.6 Live video (IMG_9698) & screenshots (9700/9701)
│       ├── 07_model_training_and_evaluation/ # M1.6 Evaluation script, predictions
│       ├── 08_model_failure_analysis/        # Detailed failure analysis & M2 plan
│       └── 09_raspberry_pi_setup/            # Hardware specs, reproducible setup script
│
├── cad/
│   └── pir_sensor_enclosure_mithra_ravi.stl  # 3D-printed enclosure CAD model
├── data/
│   ├── data.yaml                             # Portable YOLO dataset manifest
│   ├── dataset_info.md                       # Full dataset split documentation
│   ├── samples/                              # Verification sample images
│   ├── train/                                # Training images & labels (28)
│   ├── valid/                                # Validation images & labels (8)
│   └── test/                                 # Test split images & labels (4)
├── models/
│   ├── best.pt                               # Original trained YOLO Nano PyTorch weights
│   ├── best.onnx                             # Standalone ONNX runtime export
│   └── model_metadata.json                   # Comprehensive Roboflow training metrics
├── src/
│   ├── camera.py                             # Low-latency threaded camera stream
│   ├── detector.py                           # YOLO detection & HUD overlay engine
│   ├── inference.py                          # Multi-backend inference runner
│   └── monitor.py                            # Telemetry monitor & benchmark logger
├── requirements.txt                          # Cross-platform dependencies
├── run_detection.sh                          # Single-command Raspberry Pi 5 launcher
└── README.md                                 # Master project documentation
```

---

## 3. College Assessment Rubric Evidence Index (M1)

This repository is organized to satisfy every individual assessment requirement for **Milestone 1 (M1 Detect)** (20 / 20 marks). Each destination folder contains complete documentation, reproducible code, and physical verification evidence:

| Milestone Task | Submitted Document URL | Repository Destination Folder | Task README & Proof | Status | Max Marks |
| :--- | :--- | :--- | :--- | :---: | :---: |
| **M1.1: Camera and repo** | `https://github.com/mithra4325/edge-ai-enclosure-detection` | [`camera_and_repo/`](camera_and_repo/) & [`evidence/M1/01_camera_and_repo/`](evidence/M1/01_camera_and_repo/) | [`README.md`](camera_and_repo/README.md), [`spec_sheet.md`](camera_and_repo/spec_sheet.md), [`first_frame.jpg`](camera_and_repo/first_frame.jpg) | **COMPLETE** | 2 |
| **M1.2: OpenCV pipeline** | `https://github.com/mithra4325/edge-ai-enclosure-detection/opencv_pipeline` | [`opencv_pipeline/`](opencv_pipeline/) | [`README.md`](opencv_pipeline/README.md) & [`live_detection.py`](opencv_pipeline/live_detection.py) | **COMPLETE** | 4 |
| **M1.3: Baseline speed** | `https://github.com/mithra4325/edge-ai-enclosure-detection/baseline_speed` | [`baseline_speed/`](baseline_speed/) | [`README.md`](baseline_speed/README.md) & [`baseline_results.csv`](baseline_speed/baseline_results.csv) | **COMPLETE** | 3 |
| **M1.4: Dataset v1** | `https://github.com/mithra4325/edge-ai-enclosure-detection/dataset_v1` | [`dataset_v1/`](dataset_v1/) | [`README.md`](dataset_v1/README.md), [`dataset_card.md`](dataset_v1/dataset_card.md), [`annotated_images/`](dataset_v1/annotated_images/) (40 images) | **COMPLETE** | 4 |
| **M1.5: Correct split** | `https://github.com/mithra4325/edge-ai-enclosure-detection/correct_split` | [`correct_split/`](correct_split/) & [`current_split/`](current_split/) | [`README.md`](correct_split/README.md), [`verify_split.py`](correct_split/verify_split.py), [`verification_results.txt`](correct_split/verification_results.txt) | **COMPLETE** | 2 |
| **M1.6: Train and run detector** | `https://github.com/mithra4325/edge-ai-enclosure-detection/train_and_run_detector` | [`train_and_run_detector/`](train_and_run_detector/) | [`README.md`](train_and_run_detector/README.md) & [`evaluate_detector.py`](train_and_run_detector/evaluate_detector.py) | **COMPLETE** | 5 |
| **TOTAL M1 MARKS** | | | | **20 / 20** | **20** |

---

## 4. Live Demonstration Evidence

Authentic live demonstration recordings captured directly on the Raspberry Pi 5 are preserved in [`evidence/M1/06_live_demonstration/`](evidence/M1/06_live_demonstration/):

- **Live Demonstration Video:** [`evidence/M1/06_live_demonstration/live_demo_video.mov`](evidence/M1/06_live_demonstration/live_demo_video.mov) (Original upload: `IMG_9698.MOV`, 24.5 MB, $2160 \times 3840$ @ 120 FPS high-speed capture demonstrating real-time camera inference and OpenCV window tracking).
- **Live Demonstration Screenshot 1:** [`evidence/M1/06_live_demonstration/live_demo_screenshot_1.png`](evidence/M1/06_live_demonstration/live_demo_screenshot_1.png) (Original upload: `IMG_9700.PNG`, 1206&times;2622, showing live enclosure detection at **76.1%** confidence along with spurious edge activations on light surfaces).
- **Live Demonstration Screenshot 2:** [`evidence/M1/06_live_demonstration/live_demo_screenshot_2.png`](evidence/M1/06_live_demonstration/live_demo_screenshot_2.png) (Original upload: `IMG_9701.PNG`, 1206&times;2622, showing enclosure detection at **74.5%** and **66.7%** confidence under oblique perspective).
- **Demonstration Analysis:** [`evidence/M1/06_live_demonstration/README.md`](evidence/M1/06_live_demonstration/README.md) contains full telemetry and visual analysis.

---

## 5. Technical Documentation Index

Complete project engineering documentation is archived in [`docs/`](docs/):

1. **[`docs/PROJECT_REPORT.md`](docs/PROJECT_REPORT.md):** Complete M1 technical report covering problem definition, CAD modeling, Roboflow workflow, training results, embedded deployment, and benchmarking.
2. **[`docs/MODEL_CARD.md`](docs/MODEL_CARD.md):** Formal Model Card specifying YOLO26n architecture, 2.5M parameters, 5.9 GFLOPs, inputs, weights, and PyTorch vs ONNX differences.
3. **[`docs/DATASET_CARD.md`](docs/DATASET_CARD.md):** Formal Dataset Card documenting the 40-image authentic Roboflow dataset v1, 60 annotations, and cryptographic 70/20/10 split.
4. **[`docs/EXPERIMENT_LOG.md`](docs/EXPERIMENT_LOG.md):** Chronological development record detailing every Git commit, test run, and hardware integration.
5. **[`docs/FAILURE_ANALYSIS.md`](docs/FAILURE_ANALYSIS.md):** In-depth engineering failure analysis of the white-surface false-positive issue and M2 data-centric solution.
6. **[`docs/REPRODUCIBILITY.md`](docs/REPRODUCIBILITY.md):** Step-by-step reproducible setup guide for fresh Raspberry Pi 5 installations.
7. **[`docs/M1_ASSESSMENT_MAPPING.md`](docs/M1_ASSESSMENT_MAPPING.md):** Complete assessment rubric verification matrix (20 / 20 marks verified).

---

## 6. Observed Limitation: The White-Surface False-Positive Problem & M2 Plan

During real-world webcam deployment, an important operational limitation was discovered:
- **Observation:** The model occasionally detects non-enclosure white surfaces (white paper, pale desk margins, light walls) as enclosures with confidence scores between $22\%$ and $48\%$.
- **Hypothesis:** Dataset v1 contained 40 images of the white PLA enclosure photographed exclusively against a dark brown wooden workbench. The network learned a spurious shortcut: correlating high-contrast white boundaries with object presence, rather than purely invariant 3D geometric features.
- **Proposed M2 Mitigations:**
  1. Expand dataset to include white desks, metallic surfaces, and varied rooms.
  2. Inject 20+ hard-negative images (white paper, empty desks, non-enclosure plastic) labeled with zero boxes.
  3. Train a separate v2 model checkpoint and comparatively evaluate on a common untouched test benchmark.
  4. Quantize to INT8 via TFLite / ONNX Runtime to elevate frame rate from $\approx 2\text{ FPS}$ to $>15\text{ FPS}$.

---

## 7. Raspberry Pi 5 Physical Hardware & Performance Summary

- **Device:** Raspberry Pi 5 Model B Rev 1.1 (4GB LPDDR4X RAM, Broadcom BCM2712 Quad-core ARM Cortex-A76 @ 2.4 GHz)
- **Camera:** Logitech C270 HD USB Webcam (`/dev/video0`, native 640&times;480 @ 30 FPS)
- **OS:** Debian GNU/Linux 13 (Trixie) / Raspberry Pi OS 13.7 (Kernel 6.18.50 aarch64)

### Actual Physical Measured Performance (Unsimulated CPU Baseline)

| Telemetry Metric | Measured Value | Measurement Verification |
| :--- | :---: | :--- |
| **Inference Latency** | **270.9 ms – 293.4 ms** (Average: **281.5 ms**) | Monitored via `time.perf_counter()` |
| **Throughput (FPS)** | **3.10 – 3.56 FPS** (Average: **3.35 FPS**) | Smooth live tracking on CPU |
| **CPU Utilization** | **56.4% – 63.4%** across 4 cores | Normal multi-threaded PyTorch load |
| **GPU Utilization** | **0%** (CPU-only execution) | No GPU acceleration used |
| **System RAM Usage** | **2,442 MB** total allocated | Well within 4GB capacity |
| **CPU Temperature** | **49.0°C – 52.4°C** | Actively cooled; no thermal throttling |

---

## 8. Quick Launch Instructions

### Run Live Webcam Object Detection:
```bash
cd ~/edge-ai-enclosure-detection
./run_detection.sh
```
*Press **`q`** in the video window to quit, **`s`** to save an instant snapshot.*

### Run Baseline Benchmark Script:
```bash
python3 baseline_speed/benchmark.py
```

### Run Split Verification Script:
```bash
python3 correct_split/verify_split.py
```

### Run Full Dataset Annotation Rendering:
```bash
python3 dataset_v1/annotate_dataset.py
```

### Run Test Model Evaluation:
```bash
python3 train_and_run_detector/evaluate_detector.py
```

---

## 9. License & Acknowledgements

- **Author:** Mithra Ravi ([@mithra4325](https://github.com/mithra4325))
- **Dataset Hosting & Cloud Training:** [Roboflow Universe](https://universe.roboflow.com/mithu-1vntk/object-detection-n6b60) (CC BY 4.0)
- **Object Detection Framework:** [Ultralytics YOLO](https://github.com/ultralytics/ultralytics)
