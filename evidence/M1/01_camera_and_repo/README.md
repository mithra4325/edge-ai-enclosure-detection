# M1.1: Camera and Repository Setup

**Status:** **COMPLETE**

---

## 1. Purpose of the Task
The objective of Milestone 1.1 is to establish the Edge AI project repository on GitHub, verify the Raspberry Pi 5 hardware platform, connect and configure the physical USB webcam, capture an initial validation frame directly on the device, and document the complete system specification sheet supported by Git commit evidence.

## 2. What I Implemented
- Configured the project repository at `https://github.com/mithra4325/edge-ai-enclosure-detection`.
- Verified the hardware environment of the physical Raspberry Pi 5 Model B (Cortex-A76 quad-core SoC, 4GB RAM).
- Identified and initialized the Logitech C270 USB webcam via Linux V4L2 kernel device nodes (`/dev/video0`).
- Wrote a device inspection and frame capture routine that queries negotiated frame properties (640&times;480 resolution, YUYV format, 30 FPS).
- Programmatically captured and saved the device's first validation camera frame (`first_frame.jpg`).
- Preserved the original trained YOLO Nano model weights (`models/best.pt` and `models/best.onnx`) without retraining.

## 3. Hardware Used
- **Single Board Computer:** Raspberry Pi 5 Model B Rev 1.1 (Broadcom BCM2712, 4 &times; ARM Cortex-A76 @ 2.4 GHz, 4.0 GiB LPDDR4X RAM).
- **Camera Device:** Logitech C270 HD USB Webcam (`ID 046d:0825`, UVC driver).
- **Cooling:** Raspberry Pi Active Cooler (Aluminium heatsink with dynamic PWM fan).
- **Storage:** 64 GB Class 10 MicroSD card running ext4 root partition.

## 4. Software and Dependencies
- **OS:** Debian GNU/Linux 13 (Trixie) / Raspberry Pi OS 13.7 (Kernel: 6.18.50+rpt-rpi-2712 aarch64).
- **Python:** Python 3.13.5 (in isolated virtual environment with `--system-site-packages`).
- **Core Libraries:**
  - `python3-opencv` (v4.10.0)
  - `numpy` (v2.2.4)
  - `v4l-utils` (V4L2 command-line diagnostic tools)

## 5. How the Implementation Works
1. When the USB camera is connected to the Raspberry Pi 5, the kernel `uvcvideo` driver enumerates it and binds video nodes at `/dev/video0` and `/dev/video1`.
2. The capture script calls `cv2.VideoCapture(0)`, requesting an acquisition format of 640&times;480 pixels.
3. The camera performs automated white-balance and exposure negotiation during 5 warm-up frames.
4. The first stable frame is read into a NumPy BGR image matrix and saved to disk as `first_frame.jpg`.
5. Hardware telemetry (CPU model, clock frequency, RAM, temperature, kernel release) is queried from `/proc/cpuinfo`, `/sys/class/thermal/`, and `uname -a`, and recorded in `spec_sheet.md`.

## 6. How to Reproduce or Run It
To verify the camera connection and capture a fresh test frame on the Raspberry Pi 5:
```bash
# 1. Inspect connected USB video devices
lsusb | grep -i webcam
v4l2-ctl --list-devices

# 2. Run camera frame capture
cd ~/edge-ai-enclosure-detection
source venv/bin/activate
python -c "
import cv2
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
if ret:
    cv2.imwrite('evidence/M1/01_camera_and_repo/first_frame.jpg', frame)
    print('Captured frame successfully:', frame.shape)
cap.release()
"
```

## 7. Evidence Available in this Folder
- [`first_frame.jpg`](first_frame.jpg): The initial physical frame captured directly through the Logitech C270 webcam on the Raspberry Pi 5.
- [`spec_sheet.md`](spec_sheet.md): Comprehensive device hardware, operating system, and camera specification sheet.
- [`commit_evidence.md`](commit_evidence.md): Git log and commit verification showing repository authorship and deployment history.

## 8. Actual Results
- **Camera Device Node:** `/dev/video0` opened cleanly.
- **Negotiated Resolution:** 640 &times; 480 pixels.
- **Color Format:** YUYV (4:2:2).
- **Reported Frame Rate:** 30.0 FPS.
- **Repository Commit:** Verified on branch `main` (`commit 556ff11`).

## 9. Pending Items and Limitations
- **Pending Items:** None for Milestone 1.1.
- **Limitations:** The Logitech C270 is a fixed-focus USB webcam. Optimal focus distance is between 0.3 meters and 1.5 meters from the lens.
