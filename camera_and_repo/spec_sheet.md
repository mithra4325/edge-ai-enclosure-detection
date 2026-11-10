# Hardware & Camera Specification Sheet

**Project Title:** Edge AI 3D-Printed Enclosure Detection  
**Author / Student:** Mithra Ravi (`mithra4325`)  
**Target Device:** Raspberry Pi 5 Model B Rev 1.1  
**Assessment Milestone:** M1.1 — Camera and Repository  

---

## 1. Single Board Computer (SBC) Hardware Specifications

| Parameter | Specification | Physical Device Verification |
| :--- | :--- | :--- |
| **Model** | Raspberry Pi 5 Model B Rev 1.1 | Verified via `cat /proc/cpuinfo` |
| **Processor SoC** | Broadcom BCM2712 | 16nm Quad-core Application Processor |
| **CPU Core Architecture**| 4 &times; ARM Cortex-A76 | 64-bit ARMv8.2-A instruction set @ 2.4 GHz |
| **CPU Cache Hierarchy** | 512KB L2 per core, 2MB shared L3 | Supports high-throughput vectorized SIMD |
| **System Memory (RAM)** | 4.0 GiB LPDDR4X-4267 | High-bandwidth unified memory bus (sub-channel) |
| **Operating System** | Debian GNU/Linux 13 (Trixie) / Raspberry Pi OS 13.7 | Kernel: `Linux raspberrypi 6.18.50+rpt-rpi-2712 aarch64` |
| **System Python** | Python 3.13.5 | `/usr/bin/python3` (PEP 668 managed environment) |
| **Storage** | 64 GB Class 10 High-Speed MicroSD | Ext4 root filesystem on `/dev/mmcblk0p2` (27 GB free) |
| **Cooling Solution** | Raspberry Pi Active Cooler | Aluminium finned heatsink + dynamic PWM fan |
| **Baseline Thermal State**| 47.2°C – 51.5°C | Verified via `/sys/class/thermal/thermal_zone0/temp` |

---

## 2. USB Camera Specifications

| Parameter | Specification | Verification Command & Result |
| :--- | :--- | :--- |
| **Device Model** | Logitech C270 HD Webcam | `lsusb` &rarr; `ID 046d:0825 Logitech, Inc. Webcam C270` |
| **Bus Topology** | USB 2.0 Bus 001, Device 003 | Direct USB connection on Raspberry Pi 5 port |
| **Linux V4L2 Device Nodes**| `/dev/video0` (Stream), `/dev/video1` (Metadata)| Verified via `v4l2-ctl --list-devices` |
| **Kernel Driver** | `uvcvideo` (USB Video Class) | Standard Linux UVC driver module loaded |
| **Color Spaces & Formats**| YUYV 4:2:2 (`YUYV`), MJPEG (`MJPG`) | Queried via `v4l2-ctl -d /dev/video0 --list-formats-ext` |
| **Default Capture Resolution**| 640 &times; 480 pixels @ 30.000 FPS | Configured via OpenCV `VideoCapture(0)` |
| **Maximum Native Resolution** | 1280 &times; 720 pixels (720p HD) @ 30 FPS | Hardware CMOS sensor capability |

---

## 3. Initial Frame Verification

- **Filename:** `first_frame.jpg`
- **Resolution:** 640 &times; 480 pixels, 3 color channels (BGR)
- **Capture Method:** Programmatic capture using OpenCV Python bindings (`cv2.VideoCapture(0)`) on `/dev/video0`.
- **Status:** **COMPLETE** (Physical image captured and stored in this folder).
