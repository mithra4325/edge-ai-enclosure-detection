# Reproducibility Guide: Step-by-Step Deployment on Raspberry Pi 5

**Author:** Mithra Ravi (`mithra4325`)  
**Project:** Edge AI 3D-Printed Enclosure Detection  
**Target Hardware:** Raspberry Pi 5 Model B Rev 1.1 (Debian 13 Trixie / Raspberry Pi OS 13.7)  

---

## 1. Prerequisites & Hardware Checklist

Before beginning setup, ensure the following physical hardware is connected:
- **Raspberry Pi 5** (4GB or 8GB RAM recommended) with active cooling.
- **Logitech C270 HD USB Webcam** plugged directly into any USB 2.0 or USB 3.0 port.
- **Display Monitor** connected via Micro-HDMI to HDMI cable.
- **Keyboard and Mouse** connected via USB.
- **Network Connection** via Ethernet or Wi-Fi.

---

## 2. System Verification Commands

Verify the hardware and kernel nodes from the Raspberry Pi terminal:

```bash
# 1. Verify CPU and SoC
cat /proc/cpuinfo | grep -E "Model|model name" | head -n 5

# 2. Verify OS and Linux Kernel
uname -a
cat /etc/os-release

# 3. Verify USB Webcam recognition
lsusb | grep -i "Logitech"
# Expected output: Bus 001 Device 003: ID 046d:0825 Logitech, Inc. Webcam C270

# 4. Verify Linux V4L2 device nodes
v4l2-ctl --list-devices
# Expected output includes: /dev/video0 and /dev/video1 under C270 HD WEBCAM
```

---

## 3. Environment Setup & Dependency Installation

Debian 13 (Trixie) enforces PEP 668 (externally-managed environment). To ensure maximum performance and seamless integration with hardware-accelerated OpenCV, create a virtual environment that inherits system site packages:

```bash
# Step 1: Install core Debian system packages
sudo apt update
sudo apt install -y python3-pip python3-venv python3-opencv python3-numpy v4l-utils git

# Step 2: Clone the repository
cd ~
git clone https://github.com/mithra4325/edge-ai-enclosure-detection.git
cd edge-ai-enclosure-detection

# Step 3: Create isolated Python virtual environment sharing system site packages
python3 -m venv --system-site-packages venv
source venv/bin/activate

# Step 4: Install ARM64 CPU-optimized PyTorch and Ultralytics
pip install --extra-index-url https://download.pytorch.org/whl/cpu torch torchvision
pip install ultralytics onnxruntime pyyaml
```

---

## 4. Verification Tests

### Test 1: Verify Original Model Weights & Architecture
```bash
python -c "
from ultralytics import YOLO
model = YOLO('models/best.pt')
print('Model loaded successfully!')
print('Classes:', model.names)
print('Parameters:', sum(p.numel() for p in model.model.parameters()))
"
```
*Expected Output:*
```text
Model loaded successfully!
Classes: {0: 'enclosure'}
Parameters: 2504190
```

### Test 2: Verify Offline Model Inference on Sample Enclosure Image
```bash
python -c "
import cv2
from ultralytics import YOLO
model = YOLO('models/best.pt')
res = model('data/test/images/IMG_9650_HEIC.rf.95244ddfd21cd5085d78554ee80ad930.jpg', conf=0.25)
print('Detections found:', len(res[0].boxes))
print('Confidence:', [float(c) for c in res[0].boxes.conf])
"
```
*Expected Output:*
```text
Detections found: 1
Confidence: [0.9389...]
```

### Test 3: Verify USB Webcam Capture
```bash
python camera_and_repo/capture_frame.py evidence/camera/test_repro.jpg
ls -lh evidence/camera/test_repro.jpg
```

### Test 4: Verify Zero-Leakage Dataset Partition (70/20/10)
```bash
python correct_split/verify_split.py
```
*Expected Output:*
```text
=================================================================
 DATASET SPLIT & LEAKAGE VERIFICATION REPORT 
=================================================================
Total Images in Dataset: 40
  - Training Set:   28 images ( 70.0%) [Target: 70%]
  - Validation Set:  8 images ( 20.0%) [Target: 20%]
  - Test Set:        4 images ( 10.0%) [Target: 10%]
=================================================================
[SUCCESS] Dataset strictly conforms to 70/20/10 ratio with ZERO data leakage.
```

---

## 5. Launching Real-Time Live Detection

Run the primary launcher script from the repository root:

```bash
cd ~/edge-ai-enclosure-detection
./run_detection.sh
```

### Application Controls:
- **`q`** or **`ESC`**: Exit the application cleanly.
- **`s`**: Save an instant timestamped snapshot to `evidence/live_detection/`.

### Troubleshooting Display Issues:
If running through SSH without an attached display:
```bash
# To run headless while logging benchmark CSV and periodic snapshots:
python src/inference.py --model models/best.pt --source 0 --max-frames 100
```
If launching from a terminal inside the desktop GUI session:
```bash
DISPLAY=:0 ./run_detection.sh
```
