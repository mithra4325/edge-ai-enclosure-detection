# M1.6 Evidence: Live Webcam Demonstration

**Status:** **COMPLETE & VERIFIED**  
**Author / Student:** Mithra Ravi (`mithra4325`)  
**Project:** Edge AI 3D-Printed Enclosure Detection  
**Target Hardware:** Raspberry Pi 5 Model B Rev 1.1 (ARM Cortex-A76 @ 2.4 GHz)  
**Camera:** Logitech C270 HD USB Webcam (`/dev/video0`)  
**Trained Model:** Original YOLO Nano (`yolo26n`, `models/best.pt`)  

---

## 1. Overview of Live Demonstration

This folder preserves the physical, unsimulated live demonstration artifacts recorded on the Raspberry Pi 5. The demonstration proves that the complete Edge AI pipeline—from physical V4L2 USB camera frame capture to multi-threaded preprocessing, PyTorch CPU neural network forward pass, non-maximum suppression (NMS), HUD telemetry overlay rendering, and desktop GUI display—is functioning in real time on the embedded device.

The live demonstration consists of:
1. **Live Demonstration Video:** [`live_demo_video.mov`](live_demo_video.mov) (Original upload: `IMG_9698.MOV`, 24.5 MB, 2160&times;3840 @ 120 FPS high-speed capture).
2. **Live Demonstration Screenshot 1:** [`live_demo_screenshot_1.png`](live_demo_screenshot_1.png) (Original upload: `IMG_9700.PNG`, 1206&times;2622, 3.5 MB).
3. **Live Demonstration Screenshot 2:** [`live_demo_screenshot_2.png`](live_demo_screenshot_2.png) (Original upload: `IMG_9701.PNG`, 1206&times;2622, 3.4 MB).

---

## 2. Hardware and Camera Configuration

| Subsystem | Physical Hardware Details | Verification / Device Node |
| :--- | :--- | :--- |
| **SBC** | Raspberry Pi 5 Model B Rev 1.1 | Broadcom BCM2712 Quad-Core Cortex-A76 @ 2.4 GHz, 4GB LPDDR4X |
| **Camera** | Logitech C270 HD USB Webcam | USB Bus 001, Device 003 (`ID 046d:0825`), Linux `uvcvideo` driver |
| **Video Device** | `/dev/video0` (V4L2 Capture Node) | Negotiated format: YUYV 4:2:2, $640 \times 480$ pixels @ 30 FPS |
| **Display Server** | X11 / Wayland on `:0` | Live OpenCV window rendered on connected desktop monitor |
| **Cooling** | Raspberry Pi Active Cooler | Aluminium heatsink with PWM fan, maintained thermals under 52°C |

---

## 3. Explanation of On-Screen HUD Overlay & Bounding Boxes

Every frame rendered during live inference features the heads-up display (HUD) banner and localized detection boxes:

```text
+-------------------------------------------------------------------------------------------------+
| CUSTOM ENCLOSURE DETECTION                                                                      |
| Objects detected: 1                                                                             |
| FPS: 1.84                                                                                       |
| Inference latency: 454.5 ms                                                                     |
| Device: Raspberry Pi 5 CPU (ARM Cortex-A76) | CPU: 74% | Temp: 50.7C | RAM: 2880MB             |
+-------------------------------------------------------------------------------------------------+
```

- **Bounding Box (Neon Green / Magenta):** Tight coordinates $[x_1, y_1, x_2, y_2]$ indicating the spatial boundary of the detected enclosure.
- **Class Label Badge:** Shows the detected class `enclosure` alongside the model's confidence probability (e.g., `enclosure: 93.9%`).
- **Objects Detected:** Real-time count of all bounding boxes passing the $0.25$ confidence threshold in the current frame.
- **FPS (Frames Per Second):** Rolling average frame processing rate of the entire application (camera grab + letterboxing + model inference + rendering + display). Measured between **1.8 FPS and 3.4 FPS** on CPU.
- **Inference Latency:** Precise duration in milliseconds required exclusively for the neural network forward pass through the 260 convolutional layers of the YOLO Nano backbone (typically **280 ms to 560 ms** on ARM Cortex-A76 CPU).
- **Device & System Telemetry:** Live hardware diagnostics reading from Linux `/sys/class/thermal/` and `/proc/stat`.

---

## 4. Analysis of Demonstration Evidence

### A. Live Video ([`live_demo_video.mov`](live_demo_video.mov))
- **Duration & Format:** 2.3 seconds recorded at high frame-rate ($2160 \times 3840$, 120 FPS capture mode).
- **Observed Behavior:** Demonstrates the live camera feed running inside the OpenCV desktop window on the Raspberry Pi 5. The video captures the real-time interaction as objects are positioned in the field of view of the Logitech C270 webcam.
- **Verification:** Proves that the video feed is not a static playback or hardcoded simulation, but a dynamically updating optical stream.

### B. Screenshot 1 ([`live_demo_screenshot_1.png`](live_demo_screenshot_1.png))
- **Resolution:** $1206 \times 2622$ pixels.
- **Observed Behavior:** Captures the live detection system under workbench lighting. The enclosure is actively tracked with high confidence (**76.1%**).
- **Key Observation:** The screenshot also reveals additional bounding box proposals (**45.8%**, **29.1%**, **22.2%**) triggered along high-contrast pale edges in the scene. This provides direct empirical proof of the white-surface sensitivity documented in Section 5.

### C. Screenshot 2 ([`live_demo_screenshot_2.png`](live_demo_screenshot_2.png))
- **Resolution:** $1206 \times 2622$ pixels.
- **Observed Behavior:** Shows an alternate camera perspective where the enclosure is tracked at **74.5%** and **66.7%** confidence.
- **Key Observation:** Similar to Screenshot 1, bounding boxes appear around adjacent light-colored surfaces in the workspace, demonstrating the background-correlation limitation of the v1 model.

---

## 5. Visible Limitations in the Demonstration

1. **White Surface False-Positive Sensitivity:**
   - *Observation:* Pale or white surfaces in the background occasionally trigger bounding boxes with confidence scores between $22\%$ and $45\%$.
   - *Cause:* The v1 training dataset was captured with a white PLA 3D-printed enclosure against a single dark brown workbench. The network learned strong color/luminance contrast rather than exclusively invariant 3D geometric shape features (see [`08_model_failure_analysis/README.md`](../08_model_failure_analysis/README.md) for full scientific analysis).
2. **CPU Inference Latency:**
   - *Observation:* The unquantized FP32 PyTorch model runs on the ARM Cortex-A76 CPU at $\approx 454\text{ ms}$ latency ($\approx 1.8\text{ FPS}$).
   - *M2 Roadmap:* Milestone 2 will address this by exporting to INT8 quantized TFLite/ONNX to reach the target $15+$ FPS.
