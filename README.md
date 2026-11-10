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

## 5. Raspberry Pi Deployment Preparation

When transferring to a Raspberry Pi:
1. **Clone this repository** on the Raspberry Pi:
   ```bash
   git clone https://github.com/mithra4325/edge-ai-enclosure-detection.git
   cd edge-ai-enclosure-detection
   ```
2. **Install requirements** in a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
3. **Connect Camera:** Ensure Raspberry Pi Camera module or USB camera is connected.
4. **Execute Inference:**
   ```bash
   python src/inference.py --model models/best.onnx --source 0
   ```
> [!NOTE]
> Physical hardware benchmarking on the Raspberry Pi board will be conducted when returning to the college laboratory.

---

## 6. License & Acknowledgements

- **Author:** Mithra Ravi ([@mithra4325](https://github.com/mithra4325))
- **Dataset Hosting & Cloud Training:** [Roboflow Universe](https://universe.roboflow.com/mithu-1vntk/object-detection-n6b60) (CC BY 4.0)
- **Object Detection Framework:** [Ultralytics YOLO](https://github.com/ultralytics/ultralytics)
