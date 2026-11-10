# M2.6: Project Targets, Results & Edge AI Engineering Trade-offs

**Student Name:** Mithra Ravi  
**Milestone:** M2 Optimize  
**Task:** Own target and trade-off (Max marks: 3)  
**Proof Statement:** *"I show the accuracy and speed target I wrote before training, my result, and explain the trade-off in simple words"*

---

## 1. Targets Defined Before Training vs Achieved Physical Results

Before beginning data collection and model training, specific quantitative targets were established based on the real-time operational requirements of an automated 3D-printing quality inspection station:

| Project Objective | Pre-Training Target Specification | Physical Result Achieved on RPi 5 | Assessment Evaluation |
| :--- | :--- | :--- | :---: |
| **Detection Accuracy** | $\ge \mathbf{90.0\%}$ mAP @ 0.50 | **100.0%** mAP @ 0.50 (96.37% mAP@0.5:0.95) | **Target Exceeded (+10%)** |
| **Precision / Recall** | $\ge \mathbf{85.0\%}$ Precision & Recall | **100.0%** Precision / **100.0%** Recall | **Target Exceeded (+15%)** |
| **Throughput (FPS)** | $\ge \mathbf{3.0}$ FPS on Raspberry Pi 5 CPU | **3.89 FPS** (ONNX) / **3.64 FPS** (INT8) | **Target Met (+20%)** |
| **Inference Latency** | $\le \mathbf{350}$ ms per frame | **256.8 ms** (ONNX median) | **Target Met (-93 ms faster)** |
| **Model Size Footprint**| $\le \mathbf{15.0}$ MB storage | **2.72 MB** (INT8 Quantized ONNX) | **Target Exceeded (82% smaller)** |
| **Thermal Ceiling** | $\le \mathbf{65.0^\circ C}$ (Prevent thermal throttle)| **50.2°C** sustained temperature | **Safe Operating Range** |
| **Zero False Negatives**| 0 dropped enclosures on test set | **0 dropped enclosures** on test split | **Reliability Target Met** |

---

## 2. Core Edge AI Trade-offs Explained in Simple Words

In edge computing, you cannot optimize everything simultaneously. You must make deliberate engineering compromises between **Accuracy**, **Speed**, **Memory**, and **Power**. Here is how those trade-offs were balanced in this project:

### Trade-off 1: Model Size vs Accuracy (Choosing YOLO Nano over YOLO Medium)
- **The Dilemma:** Larger models (like YOLO26m with 25 million parameters) have slightly better general feature capacity, but require over 50 GFLOPs of compute.
- **My Choice:** I chose **YOLO Nano (`yolo26n`)** with only 2.5 million parameters and 5.9 GFLOPs.
- **Why It Made Sense:** Because our task is specialized (detecting one specific 3D-printed enclosure geometry rather than 80 generic COCO classes), a lightweight Nano model achieved **100% mAP@0.5** while running in **256 ms on CPU**, whereas a Medium model would have choked the Raspberry Pi CPU at less than 1 FPS.

### Trade-off 2: Precision vs Memory Bandwidth (FP32 vs INT8 Quantization)
- **The Dilemma:** Standard deep learning models store every weight as a 32-bit floating point number (FP32). 8-bit integer quantization (INT8) compresses numbers into 8-bit integers, which can introduce numerical rounding errors.
- **My Choice:** I dynamically quantized the model from FP32 to INT8.
- **Why It Made Sense:** The model size dropped by **71%** (from 9.34 MB down to **2.72 MB**), allowing the entire model weights to fit into the processor's high-speed internal cache memory. Because our trained features were distinct, mAP@0.5 remained at **100% with zero dropped detections**, while significantly reducing DRAM memory bus congestion.

### Trade-off 3: Camera Resolution vs Real-Time Responsiveness
- **The Dilemma:** The Logitech C270 camera supports 720p HD ($1280 \times 720$), but processing 1 million pixels takes longer to resize and letterbox.
- **My Choice:** Configured camera capture at $640 \times 480$ and letterboxed to the model's native $640 \times 640$ resolution.
- **Why It Made Sense:** $640 \times 480$ perfectly matches the receptive field of the YOLO Nano P3/P4 feature layers at workbench distances ($0.3\text{m} - 1.2\text{m}$), avoiding wasted CPU cycles on unnecessary downsampling.

### Trade-off 4: Frame Queue Latency vs Video Smoothness
- **The Dilemma:** Standard video streams buffer frames in memory so video looks smooth, but if inference takes 280ms, the user sees old frames from 1 second ago.
- **My Choice:** Implemented a threaded non-blocking frame grabber (`src/camera.py`) that discards buffered frames and always returns the newest frame.
- **Why It Made Sense:** In an industrial enclosure inspection line, having the newest camera frame with zero delay is vastly more important than recording smooth buffered video.

---

## 3. Summary Conclusion

By matching the compact model architecture (`yolo26n`) to the single-class detection task, using ONNX Runtime CPU vectorization, and applying INT8 quantization, the project achieved all student pre-training targets on raw Raspberry Pi 5 CPU hardware without requiring external accelerators.
