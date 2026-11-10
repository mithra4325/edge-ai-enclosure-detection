# M1.1: Camera and Hardware Spec Sheet & Repository Evidence

**Student Name:** Mithra Ravi  
**GitHub Username:** `mithra4325`  
**Repository:** [https://github.com/mithra4325/edge-ai-enclosure-detection](https://github.com/mithra4325/edge-ai-enclosure-detection)  
**Milestone:** M1 Detect  
**Task:** Camera and Repo (Max marks: 2)  
**Proof Statement:** *"I capture a frame on the device and make my own commit with the spec sheet and first frame"*

---

## 1. Hardware & Board Specifications

| Hardware Component | Specification | Technical Details |
| :--- | :--- | :--- |
| **Edge SBC Model** | **Raspberry Pi 5 Model B Rev 1.1** | Flagship Single Board Computer |
| **SoC Processor** | **Broadcom BCM2712** | 16nm process node |
| **CPU Architecture** | **Quad-core ARM Cortex-A76** | 64-bit ARMv8.2-A @ 2.4 GHz |
| **GPU / Video** | VideoCore VII @ 800 MHz | Vulkan 1.2, OpenGL ES 3.1 |
| **System Memory (RAM)**| **4.0 GiB LPDDR4X-4267** | High-bandwidth unified memory |
| **Storage Medium** | 64 GB Class 10 High-Speed MicroSD | Ext4 rootfs partition on `/dev/mmcblk0p2` |
| **Thermal Solution** | Active Cooler Heat Sink + PWM Fan | Stable baseline operating temp: 47°C – 51°C |
| **Power Supply** | Official 27W USB-C PD (5V/5A) | Full power delivery for USB 3.0 & SoC |

---

## 2. Operating System & Software Environment

- **OS Distribution:** Debian GNU/Linux 13 (Trixie) / Raspberry Pi OS 13.7
- **Kernel Version:** `Linux raspberrypi 6.18.50+rpt-rpi-2712 #1 SMP PREEMPT Debian 1:6.18.50-1+rpt1 aarch64`
- **System Python:** `Python 3.13.5` (`/usr/bin/python3`)
- **Virtual Environment:** Isolated virtualenv at `~/edge-ai-enclosure-detection/venv` (with `--system-site-packages`)
- **Computer Vision:** `OpenCV 4.10.0` (Debian ARM64 native)
- **Inference Runtime:** `PyTorch 2.15.0+cpu` & `Ultralytics 8.4.208` & `ONNX Runtime 1.31.1`

---

## 3. USB Webcam Hardware Specifications

- **Device Name:** Logitech C270 HD Webcam
- **USB Hardware ID:** `ID 046d:0825 Logitech, Inc. Webcam C270`
- **Bus Connection:** USB 2.0 Bus 001 Device 003
- **Linux Video Nodes:** `/dev/video0` (video capture streaming), `/dev/video1` (metadata)
- **V4L2 Driver:** `uvcvideo` (Linux USB Video Class driver)
- **Supported Formats:** YUYV (4:2:2) & MJPEG
- **Default Capture Resolution:** 640 &times; 480 pixels @ 30 FPS
- **Maximum Resolution:** 1280 &times; 720 (720p HD) @ 30 FPS

---

## 4. First Captured Frame Verification

The camera was opened via OpenCV `cv2.VideoCapture(0)`. The initial verification frame was captured directly on the physical Raspberry Pi 5 device and saved as evidence:

- **Saved Image:** [`first_frame.jpg`](first_frame.jpg)
- **Resolution:** 640 &times; 480 (3 channels BGR)
- **Capture Timestamp:** Verified during physical deployment session.

---

## 5. Repository & Commit Verification

- **Repository Clone Path:** `/home/forge/edge-ai-enclosure-detection`
- **Git Branch:** `main`
- **Git Remote:** `https://github.com/mithra4325/edge-ai-enclosure-detection.git`
- **Initial Deployment Commit Hash:** `556ff11`
- **Commit Message:** `"Deploy edge AI enclosure detection pipeline on Raspberry Pi 5 (M1 Milestone)"`
