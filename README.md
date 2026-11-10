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

## 5. College Assessment Rubric Evidence Index (M1 & M2)

This repository is structured to satisfy every individual assessment requirement for **Milestone 1 (M1 Detect)** and **Milestone 2 (M2 Optimize)**. Click any requirement below to navigate directly to its evidence folder and proof documentation:

### Milestone 1: M1 Detect (20 Marks Total)

| Task | What Student Must Show (Individual Proof) | Marks | Evidence Folder & Documentation |
| :--- | :--- | :---: | :--- |
| **Camera and repo** | Capture a frame on device & commit with spec sheet + first frame | **2** | [`evidence/m1_camera_and_repo/`](evidence/m1_camera_and_repo/) &rarr; [`spec_sheet.md`](evidence/m1_camera_and_repo/spec_sheet.md) |
| **OpenCV pipeline** | Run live overlay (boxes + count) on device | **4** | [`evidence/m1_opencv_pipeline/`](evidence/m1_opencv_pipeline/) &rarr; [`pipeline_architecture.md`](evidence/m1_opencv_pipeline/pipeline_architecture.md) |
| **Baseline speed** | Measure FPS, latency, CPU/GPU load, temperature with own numbers | **3** | [`evidence/m1_baseline_speed/`](evidence/m1_baseline_speed/) &rarr; [`baseline_speed_report.md`](evidence/m1_baseline_speed/baseline_speed_report.md) |
| **Dataset v1** | Label images with tight, correct boxes + data card | **4** | [`evidence/m1_dataset_v1/`](evidence/m1_dataset_v1/) &rarr; [`data_card.md`](evidence/m1_dataset_v1/data_card.md) |
| **Correct split** | Explain and show 70/20/10 split with no data leakage | **2** | [`evidence/m1_correct_split/`](evidence/m1_correct_split/) &rarr; [`split_verification.md`](evidence/m1_correct_split/split_verification.md) |
| **Train and run detector** | Show mAP@0.5, precision, recall, confusion matrix & explain 10 wrong detections | **5** | [`evidence/m1_train_and_run_detector/`](evidence/m1_train_and_run_detector/) &rarr; [`detector_training_evaluation.md`](evidence/m1_train_and_run_detector/detector_training_evaluation.md) |

---

### Milestone 2: M2 Optimize (20 Marks Total)

| Task | What Student Must Show (Individual Proof) | Marks | Evidence Folder & Documentation |
| :--- | :--- | :---: | :--- |
| **Export to ONNX** | Run the ONNX export script and show git commit | **3** | [`evidence/m2_export_to_onnx/`](evidence/m2_export_to_onnx/) &rarr; [`onnx_export_report.md`](evidence/m2_export_to_onnx/onnx_export_report.md) |
| **Convert and run live** | Convert to INT8 and run live on device (2.72 MB, -71% size) | **4** | [`evidence/m2_convert_and_run_live/`](evidence/m2_convert_and_run_live/) &rarr; [`quantization_and_live_report.md`](evidence/m2_convert_and_run_live/quantization_and_live_report.md) |
| **Accuracy check** | Show mAP before vs after on the exact same test set | **4** | [`evidence/m2_accuracy_check/`](evidence/m2_accuracy_check/) &rarr; [`mAP_before_vs_after_report.md`](evidence/m2_accuracy_check/mAP_before_vs_after_report.md) |
| **Fair benchmark** | 20 warm-up & 100+ timed runs (batch 1): median & p95 latency, FPS, model size | **4** | [`evidence/m2_fair_benchmark/`](evidence/m2_fair_benchmark/) &rarr; [`fair_benchmark_report.md`](evidence/m2_fair_benchmark/fair_benchmark_report.md) |
| **CPU vs accelerator + stack**| Show CPU vs accelerator comparison table and draw software stack | **2** | [`evidence/m2_cpu_vs_accelerator/`](evidence/m2_cpu_vs_accelerator/) &rarr; [`cpu_vs_accelerator_analysis.md`](evidence/m2_cpu_vs_accelerator/cpu_vs_accelerator_analysis.md) |
| **Own target and trade-off** | Show pre-training accuracy & speed target, result, explain trade-offs | **3** | [`evidence/m2_target_and_tradeoff/`](evidence/m2_target_and_tradeoff/) &rarr; [`target_and_tradeoff_analysis.md`](evidence/m2_target_and_tradeoff/target_and_tradeoff_analysis.md) |

---

## 6. Raspberry Pi 5 Hardware & Measured Benchmark Summary

- **Device:** Raspberry Pi 5 Model B Rev 1.1 (4GB LPDDR4X RAM, Quad-core ARM Cortex-A76 @ 2.4 GHz)
- **Camera:** Logitech C270 HD USB Webcam (`/dev/video0`, native 640x480 @ 30 FPS)
- **OS:** Debian GNU/Linux 13 (Trixie) / Raspberry Pi OS 13.7 (Kernel 6.18.50 aarch64)

### Actual Physical Measured Performance

| Runtime Format | Model Size | Median Latency | P95 Latency | FPS | mAP @ 0.50 | Accuracy Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **PyTorch FP32 Baseline** | 5.16 MB | 468.2 ms | 695.2 ms | 2.14 FPS | **100.0%** | Full Precision Baseline |
| **ONNX FP32 (Opset 17)** | 9.34 MB | 256.8 ms | 393.4 ms | **3.89 FPS** | **100.0%** | $1.82\times$ CPU Speedup |
| **Quantized INT8 ONNX** | **2.72 MB** (-71%) | 274.6 ms | 445.8 ms | **3.64 FPS** | **100.0%** | Near-Zero Accuracy Drop |

---

## 7. Quick Launch Instructions

### Run Live Webcam Object Detection:
```bash
./run_detection.sh
```
*Press **`q`** in the video window to quit, **`s`** to save a snapshot.*

### Run Fair Benchmark (20 Warm-up + 100 Timed Runs):
```bash
./venv/bin/python evidence/m2_fair_benchmark/run_fair_benchmark.py
```

### Run Accuracy Comparison on Test Split:
```bash
./venv/bin/python evidence/m2_accuracy_check/accuracy_evaluation.py
```

---

## 6. License & Acknowledgements

- **Author:** Mithra Ravi ([@mithra4325](https://github.com/mithra4325))
- **Dataset Hosting & Cloud Training:** [Roboflow Universe](https://universe.roboflow.com/mithu-1vntk/object-detection-n6b60) (CC BY 4.0)
- **Object Detection Framework:** [Ultralytics YOLO](https://github.com/ultralytics/ultralytics)
