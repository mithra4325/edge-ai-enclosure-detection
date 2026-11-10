# M1.9 Evidence: Raspberry Pi 5 System Setup & Reproducibility Guide

**Status:** **COMPLETE & VERIFIED**  
**Author / Student:** Mithra Ravi (`mithra4325`)  
**Project:** Edge AI 3D-Printed Enclosure Detection  
**Target Hardware:** Raspberry Pi 5 Model B Rev 1.1 (ARM Cortex-A76 @ 2.4 GHz)  
**Camera:** Logitech C270 HD USB Webcam  

---

## 1. Verified Hardware Specifications

All hardware specifications were verified through Linux system inspection utilities:

| Component | Physical Specification | Inspection Command & Output |
| :--- | :--- | :--- |
| **SBC Model** | Raspberry Pi 5 Model B Rev 1.1 | `cat /proc/cpuinfo` &rarr; `Model: Raspberry Pi 5 Model B Rev 1.1` |
| **SoC Processor** | Broadcom BCM2712 (16nm process) | 4 &times; ARM Cortex-A76 64-bit cores @ 2.4 GHz |
| **Instruction Set**| ARMv8.2-A with ARM NEON SIMD vector engines | Hardware vectorized float arithmetic |
| **System Memory** | 4.0 GiB LPDDR4X-4267 SDRAM | `free -h` &rarr; `4.0Gi total`, `845Mi available` |
| **Storage** | 64 GB Class 10 High-Speed MicroSD | `df -h /` &rarr; `57G total, 26G available (ext4)` |
| **Thermal System**| Raspberry Pi Active Cooler | Heatsink + dynamic PWM fan; load temps 48°C – 52°C |
| **Webcam Model** | Logitech C270 HD USB Webcam | `lsusb` &rarr; `ID 046d:0825 Logitech, Inc. Webcam C270` |
| **Camera Port** | USB 2.0 (Bus 001, Device 003) | `v4l2-ctl --list-devices` &rarr; `/dev/video0`, `/dev/video1` |

---

## 2. Operating System & Software Stack

| Layer | Environment Details | Version / State |
| :--- | :--- | :--- |
| **Operating System** | Debian GNU/Linux 13 (Trixie) / Raspberry Pi OS | 13.7 (64-bit `aarch64`) |
| **Kernel Release** | Linux 6.18.50+rpt-rpi-2712 | Preempt RT enabled |
| **Base Python** | Python 3.13.5 | System Python in `/usr/bin/python3` (PEP 668 managed) |
| **Virtual Env** | `/home/forge/edge-ai-enclosure-detection/venv` | Isolated environment with `--system-site-packages` |
| **OpenCV** | `python3-opencv` (Debian native aarch64 build) | **4.10.0** (V4L2 backend with hardware acceleration) |
| **NumPy** | NumPy (Debian native aarch64 build) | **2.2.4** |
| **Deep Learning** | PyTorch CPU-only wheel | **2.15.0+cpu** |
| **Detection Engine**| Ultralytics YOLO | **8.4.208** |
| **Inference Runtime**| ONNX Runtime | **1.31.1** |
| **Display Server** | X11 / Wayland on `:0` | Desktop session active |

---

## 3. Step-by-Step Reproducible Setup Guide

To reproduce this environment on a fresh Raspberry Pi 5 running Raspberry Pi OS (Debian 13 Trixie):

### Step 1: Install System Packages
```bash
sudo apt update
sudo apt install -y python3-pip python3-venv python3-opencv python3-numpy v4l-utils git
```

### Step 2: Clone the Project Repository
```bash
git clone https://github.com/mithra4325/edge-ai-enclosure-detection.git
cd edge-ai-enclosure-detection
```

### Step 3: Create Virtual Environment with System Site Packages
```bash
# Debian Trixie enforces PEP 668. Using --system-site-packages allows
# the venv to share the high-performance Debian native OpenCV 4.10 without recompilation.
python3 -m venv --system-site-packages venv
source venv/bin/activate
```

### Step 4: Install CPU-Optimized Deep Learning Dependencies
```bash
# Install PyTorch CPU wheel specifically built for aarch64
pip install --extra-index-url https://download.pytorch.org/whl/cpu torch torchvision
pip install ultralytics onnxruntime pyyaml
```

### Step 5: Verify Camera Device
```bash
# Check USB connection and V4L2 device nodes
lsusb | grep -i "Logitech"
v4l2-ctl --list-devices
```

### Step 6: Launch Real-Time Enclosure Detection
```bash
./run_detection.sh
```

---

## 4. Key Engineering Resolutions

1. **PEP 668 Externally-Managed Environment Resolution:**
   - Debian 13 blocks standard `pip install` in the global environment.
   - *Resolution:* Created a virtual environment using `python3 -m venv --system-site-packages venv`. This allows seamless access to the native Debian `python3-opencv` bindings while keeping user packages cleanly encapsulated.
2. **PyTorch Wheel CUDA Bloat Avoidance:**
   - Standard `pip install torch` attempts to resolve 4GB of x86_64 CUDA binaries incompatible with ARM64 CPU.
   - *Resolution:* Targeted `--extra-index-url https://download.pytorch.org/whl/cpu`, installing a lightweight, pure-CPU PyTorch 2.15.0 build tailored for ARM NEON SIMD acceleration.
3. **OpenCV V4L2 Queue Buffer Lag:**
   - Standard `cv2.VideoCapture` accumulates 4-5 internal buffer frames, causing 1.5 seconds of perceived motion lag.
   - *Resolution:* Implemented a threaded `WebcamStream` class in [`src/camera.py`](../../src/camera.py) with `CAP_PROP_BUFFERSIZE = 1` and background daemon thread reading, delivering fresh zero-latency frames on demand.
