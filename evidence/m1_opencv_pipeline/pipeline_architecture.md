# M1.2: OpenCV Pipeline & Live Overlay Evidence

**Student Name:** Mithra Ravi  
**Milestone:** M1 Detect  
**Task:** OpenCV pipeline (Max marks: 4)  
**Proof Statement:** *"I run the live overlay (boxes + count) on the device myself"*

---

## 1. Pipeline Overview

The live object detection application uses a multi-threaded, low-latency OpenCV and Python pipeline deployed on the Raspberry Pi 5. The pipeline interfaces directly with the Logitech C270 USB webcam, feeds frames into the fine-tuned YOLO Nano (`yolo26n`) model, extracts detected bounding boxes and confidence scores, and renders a telemetry HUD overlay on the display.

```
+------------------+      +-------------------+      +--------------------+
|  Logitech C270   | ---> |   WebcamStream    | ---> | EnclosureDetector  |
|  (/dev/video0)   |      | Threaded Buffer=1 |      | (YOLO Nano 640x640)|
+------------------+      +-------------------+      +--------------------+
                                                               |
                                                               v
+------------------+      +-------------------+      +--------------------+
|   OpenCV Window  | <--- |   HUD Overlay &   | <--- |   SystemMonitor    |
|   Display (:0)   |      |   Bounding Boxes  |      | (FPS, Latency, C)  |
+------------------+      +-------------------+      +--------------------+
```

---

## 2. Key Components of the Pipeline

1. **Threaded Frame Acquisition (`src/camera.py`):**
   - Standard OpenCV `VideoCapture` buffers 4–5 frames in the Linux V4L2 queue by default. When model inference takes ~250–280ms, buffered frames create an artificial 1.5-second lag behind real time.
   - To eliminate buffer lag, `WebcamStream` continuously grabs the newest frame in an isolated daemon thread with `cv2.CAP_PROP_BUFFERSIZE = 1`. The inference loop always receives the freshest available frame with zero queue delay.

2. **YOLO Nano Inference (`src/detector.py`):**
   - Loads the original trained weights (`models/best.pt` or `models/best.onnx`).
   - Frame is resized to model native resolution ($640 \times 640$) via auto-letterbox maintaining aspect ratio.
   - Non-Maximum Suppression (NMS) filters duplicate overlapping boxes using IoU threshold `0.45` and confidence threshold `0.25`.

3. **Bounding Box & HUD Annotation:**
   - **Bounding Boxes:** High-visibility neon green boxes (`RGB: [0, 255, 128]`) drawn around each detected custom 3D-printed enclosure.
   - **Class Label Badge:** Solid background rectangle with contrasting text indicating `enclosure: XX.X%`.
   - **HUD Banner:** Semi-transparent top banner displaying:
     - `ENCLOSURE DETECTION`
     - `Objects detected: <COUNT>` (dynamic integer counter)
     - `FPS: <MEASURED_FPS>` (exponential rolling average)
     - `Inference latency: <LATENCY_MS> ms`
     - System hardware telemetry (CPU %, Temperature, RAM used).

---

## 3. Individual Evidence Screenshots

The following live camera frames demonstrate the live overlay running on the Raspberry Pi 5 with varying enclosure positions and object counts:

### Evidence Frame 1 (Single / Multiple Enclosures)
![Live Overlay 1](live_overlay_1.jpg)
- **Objects detected:** 5 enclosures detected simultaneously
- **Measured Latency:** ~277 ms (3.0 FPS)
- **CPU Temp:** 49.6°C

### Evidence Frame 2
![Live Overlay 2](live_overlay_2.jpg)
- **Objects detected:** Real-time dynamic count update
- **Confidence range:** 75% – 95%
- **Overlay:** Clean HUD banner and neon bounding boxes

### Evidence Frame 3
![Live Overlay 3](live_overlay_3.jpg)
- **Objects detected:** 7 enclosures detected
- **Confidences:** Up to 88.5%
- **Verification:** High contrast bounding box placement matching physical enclosure orientation.

---

## 4. Execution Command

To run the live pipeline on the Raspberry Pi 5:
```bash
./run_detection.sh
```
*Press `q` inside the video window to quit cleanly.*
