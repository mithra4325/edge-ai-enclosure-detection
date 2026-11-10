# M1.2: Real-Time OpenCV Detection Pipeline

**Status:** **COMPLETE**

---

## 1. Purpose of the Task
The objective of Milestone 1.2 is to build, execute, and verify a complete real-time computer vision detection pipeline on the physical Raspberry Pi 5. The pipeline continuously captures live frames from the Logitech C270 USB webcam using OpenCV, feeds them into the trained YOLO Nano (`yolo26n`) model, generates bounding boxes around detected custom 3D-printed enclosures, displays confidence percentages, counts detected objects, and overlays live FPS and latency telemetry directly on the display.

## 2. What I Implemented
- **Low-Latency Threaded Camera Ingestion (`camera.py`):** Implemented `WebcamStream`, an isolated background capture thread that drops stale buffered frames (`cv2.CAP_PROP_BUFFERSIZE = 1`) so that the detector always receives real-time frames with zero queue delay.
- **Detector & Annotation Engine (`detector.py`):** Integrates the original trained YOLO Nano weights (`models/best.pt`), resizes frames with letterbox aspect-ratio preservation, applies Non-Maximum Suppression (NMS IoU: 0.45, Conf: 0.25), and draws high-contrast neon green bounding boxes with confidence badges.
- **HUD Telemetry Overlay:** Built a top semi-transparent dashboard banner displaying:
  - Header: `ENCLOSURE DETECTION`
  - Dynamic Object Counter: `Objects detected: N`
  - Real-Time FPS: `FPS: XX.X`
  - Inference Latency: `Inference latency: XX.X ms`
  - Hardware Diagnostics: CPU usage %, temperature °C, and RAM usage MB.
- **Main Inference Controller (`live_detection.py`):** Provides CLI flags for camera index, confidence thresholds, evidence snapshot export, and graceful exit on `q`.

## 3. Hardware Used
- **Device:** Raspberry Pi 5 Model B Rev 1.1 (Quad-core ARM Cortex-A76 @ 2.4 GHz, 4GB LPDDR4X RAM).
- **Camera:** Logitech C270 HD USB Webcam (`/dev/video0`, native 640&times;480 @ 30 FPS).
- **Target Object:** Custom 3D-printed PIR sensor enclosure printed in black PLA filament.

## 4. Software and Dependencies
- **OS:** Debian GNU/Linux 13 (Trixie) / Raspberry Pi OS 13.7.
- **Python:** Python 3.13.5 in project virtual environment (`venv`).
- **Dependencies (`requirements.txt`):**
  - `opencv-python` (v4.10.0 native ARM64 bindings)
  - `torch` (v2.15.0+cpu ARM64)
  - `ultralytics` (v8.4.208)
  - `numpy` (v2.2.4)
  - `psutil` (v7.0.0)

## 5. How the Implementation Works
```
+--------------------+        +---------------------+        +--------------------+
| Logitech C270 USB  | -----> |    WebcamStream     | -----> |  EnclosureDetector |
| (/dev/video0)      |        | Threaded (Buffer=1) |        |  (YOLO Nano 640)   |
+--------------------+        +---------------------+        +--------------------+
                                                                        |
                                                                        v
+--------------------+        +---------------------+        +--------------------+
|   OpenCV Display   | <----- |     HUD Banner      | <----- | Detections & Boxes |
|   Window (:0)      |        |   Overlay Renderer  |        | (Class, Conf, BBox)|
+--------------------+        +---------------------+        +--------------------+
```
1. `WebcamStream` continuously captures frames in a background thread and replaces the internal frame buffer with the freshest frame.
2. `EnclosureDetector.detect(frame)` converts the BGR frame to RGB, letterboxes to $640 \times 640$, passes it through the PyTorch YOLO backbone on the Cortex-A76 CPU, and runs NMS.
3. Coordinates are scaled back to native $640 \times 480$ frame dimensions.
4. `EnclosureDetector.annotate_frame()` renders neon green bounding boxes (`BGR: [0, 255, 128]`), label badges (`enclosure: 95.4%`), and the HUD telemetry banner.
5. The window updates live via `cv2.imshow()`. The user can quit cleanly anytime by pressing `q`.

## 6. How to Reproduce or Run It
From the project root on the Raspberry Pi 5:
```bash
# 1. Activate environment
source venv/bin/activate

# 2. Run the live detection pipeline with GUI display
python opencv_pipeline/live_detection.py --model models/best.pt --source 0 --show

# 3. Alternatively, run with one-click launcher
./run_detection.sh
```
- Press **`q`** in the video window to quit.
- Press **`s`** to save an instant snapshot.

## 7. Evidence Available in this Folder
- [`camera.py`](camera.py): Modular low-latency threaded camera capture class.
- [`detector.py`](detector.py): Modular enclosure detection and HUD overlay rendering engine.
- [`live_detection.py`](live_detection.py): Executable pipeline engine supporting live camera and static images.
- [`requirements.txt`](requirements.txt): Pinned dependencies for the OpenCV pipeline.
- [`live_overlay_1.jpg`](live_overlay_1.jpg): Live camera frame showing 5 detected enclosures with bounding boxes and HUD.
- [`live_overlay_2.jpg`](live_overlay_2.jpg): Live camera frame showing real-time object tracking and confidence scores.
- [`live_overlay_3.jpg`](live_overlay_3.jpg): Live camera frame showing 7 detected enclosures with up to 88.5% confidence.
- [`offline_prediction.jpg`](offline_prediction.jpg): High-resolution offline test verification on held-out sample image (93.9% confidence).

## 8. Actual Results
- **Camera Feed:** Active and stable at 640&times;480 resolution.
- **Bounding Boxes:** Tightly fitted around visible 3D-printed enclosures.
- **Confidence Scores:** Measured between **76.5% and 95.4%** across tests.
- **Object Counting:** Dynamically increments/decrements as enclosures enter or leave the camera's field of view.
- **Measured FPS:** Stable **3.3 – 3.5 FPS** on raw Raspberry Pi 5 CPU.
- **Inference Latency:** Average **280 ms** per frame.

## 9. Pending Items and Limitations
- **Pending Items:** None for Milestone 1.2.
- **Limitations:** Inference runs on the CPU. While 3.5 FPS is sufficient for conveyor-belt inspection, acceleration to >30 FPS will be addressed in Milestone 2 optimizations.
