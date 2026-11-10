# Experiment Log: Chronological Development Record

**Project Title:** Edge AI 3D-Printed Enclosure Detection  
**Author / Developer:** Mithra Ravi (`mithra4325`)  
**Hardware Platform:** Raspberry Pi 5 Model B Rev 1.1 (ARM Cortex-A76 @ 2.4 GHz)  
**Milestone:** Milestone 1 (M1 Detect)  

---

## 1. Development Chronology & Milestones

This log provides an auditable, chronological record of every engineering milestone, script execution, hardware integration, and Git commit. All timestamps correspond to actual verified Git commits and system logs.

---

### Phase 1: CAD Design & Roboflow Dataset Curation
- **Date & Time:** November 10, 2026 — 14:00 to 15:26 IST
- **Actions Performed:**
  - Designed the physical PIR sensor camera enclosure in CAD (`cad/pir_sensor_enclosure_mithra_ravi.stl`).
  - 3D-printed the physical enclosure using white PLA filament.
  - Photographed 40 physical images of the enclosure under varying orientations and angles on a brown wooden workbench.
  - Uploaded captures to Roboflow Workspace `mithu-1vntk`, Project `object-detection-n6b60`.
  - Manually annotated 60 bounding box instances with tight perimeter fits.
  - Partitioned dataset into 28 train (70%), 8 valid (20%), and 4 test (10%) splits.
  - Trained YOLO Nano (`yolo26n`) model for 218 epochs on Roboflow cloud infrastructure.
  - Achieved validation metrics: **100.0% mAP@0.5**, **96.37% mAP@0.5:0.95**, **100.0% Precision**, **100.0% Recall**.
  - Exported original PyTorch weights (`best.pt`) and standalone ONNX graph (`best.onnx`).

---

### Phase 2: Repository Inception & Initial Model Commit
- **Commit:** [`8381094`](https://github.com/mithra4325/edge-ai-enclosure-detection/commit/8381094)
- **Timestamp:** 2026-11-10 15:29:23 +0530
- **Summary:** Initialized Git repository with original model weights, Roboflow dataset export (`data.yaml`, `train/`, `valid/`, `test/`), CAD STL file, and model metadata manifest (`models/model_metadata.json`).

---

### Phase 3: Hardware Verification & Core Pipeline Engineering
- **Commit:** [`556ff11`](https://github.com/mithra4325/edge-ai-enclosure-detection/commit/556ff11)
- **Timestamp:** 2026-11-10 16:00:41 +0530
- **Actions Performed:**
  - Configured Python 3.13.5 virtual environment (`venv`) with `--system-site-packages` to link Debian native OpenCV 4.10.0 and NumPy 2.2.4 without compilation overhead.
  - Installed lightweight PyTorch 2.15.0+cpu wheel built for ARM64 NEON vector engines.
  - Identified and initialized Logitech C270 USB webcam on `/dev/video0`.
  - Developed `src/camera.py`: implemented threaded non-blocking frame grabbing with internal buffer limit 1 to eliminate V4L2 queue latency.
  - Developed `src/detector.py`: implemented YOLO Nano loader, bounding box rendering, and semi-transparent HUD overlay.
  - Developed `src/monitor.py`: implemented system telemetry monitor reading CPU load, RAM allocation, and thermal zone temperatures.
  - Created single-command bash launcher: `run_detection.sh`.

---

### Phase 4: Initial Evidence Consolidation
- **Commit:** [`227bf8a`](https://github.com/mithra4325/edge-ai-enclosure-detection/commit/227bf8a)
- **Timestamp:** 2026-11-10 16:13:36 +0530
- **Summary:** Created baseline assessment evidence folders and reports.

---

### Phase 5: Submission URL Structure Alignment
- **Commit:** [`b5ace2e`](https://github.com/mithra4325/edge-ai-enclosure-detection/commit/b5ace2e)
- **Timestamp:** 2026-11-10 16:38:18 +0530
- **Actions Performed:**
  - Structured folders to match college assessment document links: `opencv_pipeline/`, `baseline_speed/`, `dataset_v1/`, `train_and_run_detector/`.
  - Added standalone benchmark runner `baseline_speed/benchmark.py` and evaluation script `train_and_run_detector/evaluate_detector.py`.
  - Preserved original weights with zero modification.

---

### Phase 6: Root Folders & Full 40 Annotated Dataset Upload
- **Commit:** [`33a7c8a`](https://github.com/mithra4325/edge-ai-enclosure-detection/commit/33a7c8a)
- **Timestamp:** 2026-11-10 17:47:26 +0530
- **Actions Performed:**
  - Created root `camera_and_repo/` with spec sheet, capture script, and first frame.
  - Created root `correct_split/` and `current_split/` with `verify_split.py` and SHA-256 cryptographic proof.
  - Developed `dataset_v1/annotate_dataset.py` and generated **all 40 visually annotated images** with Roboflow magenta `#ff1493` bounding boxes across `dataset_v1/annotated_images/train/`, `valid/`, and `test/`.

---

### Phase 7: Live HUD Overlay Formatting & Continuous Benchmarking
- **Commit:** [`c1fc46e`](https://github.com/mithra4325/edge-ai-enclosure-detection/commit/c1fc46e)
- **Timestamp:** 2026-11-10 17:56:41 +0530
- **Actions Performed:**
  - Updated HUD overlay in `src/detector.py` and `opencv_pipeline/detector.py` to match exact required 5-line telemetry format.
  - Enabled desktop GUI window display on `DISPLAY=:0`.
  - Executed continuous live webcam detection and logged real telemetry to `evidence/benchmark/baseline_results.csv`.

---

### Phase 8: User Live Demonstration Evidence Upload
- **Commits:** [`7f1810d`](https://github.com/mithra4325/edge-ai-enclosure-detection/commit/7f1810d) & [`31cebcd`](https://github.com/mithra4325/edge-ai-enclosure-detection/commit/31cebcd)
- **Timestamps:** 2026-11-10 18:30:37 & 18:31:34 +0530
- **Actions Performed:**
  - Uploaded live demonstration video: `IMG_9698.MOV` (24.5 MB).
  - Uploaded live demonstration screenshot 1: `IMG_9700.PNG` (3.5 MB).
  - Uploaded live demonstration screenshot 2: `IMG_9701.PNG` (3.4 MB).
  - Fast-forward merged into local repository and mirrored into `evidence/M1/06_live_demonstration/`.
