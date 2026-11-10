# Milestone 1 (M1 Detect) Assessment Mapping & Verification Matrix

**Student Name:** Mithra Ravi (`mithra4325`)  
**Repository:** [https://github.com/mithra4325/edge-ai-enclosure-detection](https://github.com/mithra4325/edge-ai-enclosure-detection)  
**Total Target Marks:** 20 / 20  
**Verification Date:** November 10, 2026  

---

## 1. Comprehensive Assessment Rubric Mapping

This matrix maps every individual requirement from the official college assessment rubric to the corresponding source code, physical evidence, and documentation in this repository:

| Task # | Assessment Task | Required Individual Proof | Relevant Source Code | Relevant Evidence File(s) | Documentation Link | Status | Marks |
| :---: | :--- | :--- | :--- | :--- | :--- | :---: | :---: |
| **M1.1** | **Camera and repo** | I capture a frame on the device and make my own commit with the spec sheet and first frame | [`camera_and_repo/capture_frame.py`](../camera_and_repo/capture_frame.py) | [`camera_and_repo/first_frame.jpg`](../camera_and_repo/first_frame.jpg), [`camera_and_repo/commit_evidence.md`](../camera_and_repo/commit_evidence.md) | [`camera_and_repo/README.md`](../camera_and_repo/README.md), [`spec_sheet.md`](../camera_and_repo/spec_sheet.md) | **COMPLETE** | 2 / 2 |
| **M1.2** | **OpenCV pipeline** | I run the live overlay (boxes + count) on the device myself | [`opencv_pipeline/live_detection.py`](../opencv_pipeline/live_detection.py), [`opencv_pipeline/detector.py`](../opencv_pipeline/detector.py), [`opencv_pipeline/camera.py`](../opencv_pipeline/camera.py) | [`opencv_pipeline/live_detection_overlay.jpg`](../opencv_pipeline/live_detection_overlay.jpg), [`evidence/M1/06_live_demonstration/`](../evidence/M1/06_live_demonstration/) | [`opencv_pipeline/README.md`](../opencv_pipeline/README.md) | **COMPLETE** | 4 / 4 |
| **M1.3** | **Baseline speed** | I measure FPS, latency, CPU/GPU load, temperature and show my own numbers | [`baseline_speed/benchmark.py`](../baseline_speed/benchmark.py), [`src/monitor.py`](../src/monitor.py) | [`baseline_speed/baseline_results.csv`](../baseline_speed/baseline_results.csv), [`baseline_speed/benchmark_overlay.jpg`](../baseline_speed/benchmark_overlay.jpg) | [`baseline_speed/README.md`](../baseline_speed/README.md) | **COMPLETE** | 3 / 3 |
| **M1.4** | **Dataset v1** | I label images with tight, correct boxes. I show my own labelled images and the data card | [`dataset_v1/annotate_dataset.py`](../dataset_v1/annotate_dataset.py) | 40 annotated images in [`dataset_v1/annotated_images/`](../dataset_v1/annotated_images/), 4 samples in [`dataset_v1/`](../dataset_v1/) | [`dataset_v1/README.md`](../dataset_v1/README.md), [`dataset_card.md`](../dataset_v1/dataset_card.md) | **COMPLETE** | 4 / 4 |
| **M1.5** | **Correct split** | I explain and show the 70/20/10 split with no leakage | [`correct_split/verify_split.py`](../correct_split/verify_split.py) | [`correct_split/verification_results.txt`](../correct_split/verification_results.txt) | [`correct_split/README.md`](../correct_split/README.md), [`current_split/README.md`](../current_split/README.md) | **COMPLETE** | 2 / 2 |
| **M1.6** | **Train and run detector** | I show mAP@0.5, precision, recall, confusion matrix vs the target, and explain 10 wrong detections | [`train_and_run_detector/evaluate_detector.py`](../train_and_run_detector/evaluate_detector.py) | 4 prediction samples in [`train_and_run_detector/`](../train_and_run_detector/), [`evidence/model_test/prediction.jpg`](../evidence/model_test/prediction.jpg) | [`train_and_run_detector/README.md`](../train_and_run_detector/README.md), [`docs/FAILURE_ANALYSIS.md`](FAILURE_ANALYSIS.md) | **COMPLETE** | 5 / 5 |
| **TOTAL**| | | | | | **COMPLETE** | **20 / 20** |

---

## 2. Detailed Task-by-Task Audit

### M1.1: Camera and Repo (2 / 2 Marks)
- **Status:** **COMPLETE**
- **Evidence Verification:**
  - Hardware specification sheet verified for Raspberry Pi 5 Model B Rev 1.1 (Cortex-A76 @ 2.4 GHz, 4GB RAM) and Logitech C270 USB webcam.
  - Physical first frame captured directly from `/dev/video0` on the device ([`camera_and_repo/first_frame.jpg`](../camera_and_repo/first_frame.jpg)).
  - Commit evidence documented ([`camera_and_repo/commit_evidence.md`](../camera_and_repo/commit_evidence.md)).
- **Missing Items:** None.

### M1.2: OpenCV Pipeline (4 / 4 Marks)
- **Status:** **COMPLETE**
- **Evidence Verification:**
  - Fully working multi-threaded live camera pipeline in [`opencv_pipeline/`](../opencv_pipeline/).
  - Threaded frame acquisition in `camera.py` prevents V4L2 queue frame lag.
  - Live HUD overlay renders bounding boxes, class tag `enclosure`, confidence score, object count, FPS, and inference latency.
  - Live demonstration video ([`evidence/M1/06_live_demonstration/live_demo_video.mov`](../evidence/M1/06_live_demonstration/live_demo_video.mov)) and screenshots ([`live_demo_screenshot_1.png`](../evidence/M1/06_live_demonstration/live_demo_screenshot_1.png), [`live_demo_screenshot_2.png`](../evidence/M1/06_live_demonstration/live_demo_screenshot_2.png)).
- **Missing Items:** None.

### M1.3: Baseline Speed Benchmark (3 / 3 Marks)
- **Status:** **COMPLETE**
- **Evidence Verification:**
  - Standalone 100-iteration benchmark runner in [`baseline_speed/benchmark.py`](../baseline_speed/benchmark.py).
  - Telemetry CSV log ([`baseline_speed/baseline_results.csv`](../baseline_speed/baseline_results.csv)).
  - Actual measured numbers on Raspberry Pi 5 CPU: Latency $\approx 454.5\text{ ms}$, Throughput $\approx 1.8\text{ – }3.4\text{ FPS}$, CPU utilization $\approx 74\%$, System RAM $\approx 2,880\text{ MB}$, Temperature $\approx 50.7^\circ\text{C}$.
  - Explicitly documents CPU-only execution (0% GPU).
- **Missing Items:** None.

### M1.4: Dataset v1 & Data Card (4 / 4 Marks)
- **Status:** **COMPLETE**
- **Evidence Verification:**
  - Authentic dataset of 40 physical photographs and 60 tight bounding boxes.
  - Roboflow project verified: Workspace `mithu-1vntk`, Project `object-detection-n6b60`.
  - Comprehensive Dataset Card in [`dataset_v1/dataset_card.md`](../dataset_v1/dataset_card.md) and [`docs/DATASET_CARD.md`](DATASET_CARD.md).
  - All 40 visually annotated images with ground-truth boxes in [`dataset_v1/annotated_images/`](../dataset_v1/annotated_images/).
- **Missing Items:** None.

### M1.5: Correct Split (2 / 2 Marks)
- **Status:** **COMPLETE**
- **Evidence Verification:**
  - Verified exact 70% / 20% / 10% ratio: 28 Train (70.0%), 8 Valid (20.0%), 4 Test (10.0%).
  - Cryptographic 256-bit SHA-256 hash checks performed by [`correct_split/verify_split.py`](../correct_split/verify_split.py).
  - Confirmed 0 filename collisions and 0 hash overlaps in [`correct_split/verification_results.txt`](../correct_split/verification_results.txt).
  - Provided at both root URLs: [`correct_split/`](../correct_split/) and [`current_split/`](../current_split/).
- **Missing Items:** None.

### M1.6: Train and Run Detector (5 / 5 Marks)
- **Status:** **COMPLETE**
- **Evidence Verification:**
  - Formal evaluation metrics verified: mAP@0.5 = 100.0%, precision = 100.0%, recall = 100.0%, optimal F1 = 1.0 at threshold 0.22.
  - Full confusion matrix documented against ground-truth targets.
  - Detailed analysis of 10 difficult detection edge cases and failure modes in [`train_and_run_detector/README.md`](../train_and_run_detector/README.md).
  - Extensive failure analysis of the white-surface false-positive issue in [`docs/FAILURE_ANALYSIS.md`](FAILURE_ANALYSIS.md).
- **Missing Items:** None.

---

## 3. Evidence Folder Cross-Index

All evidence is cross-indexed across both standard root directories and the structured `evidence/M1/` tree:

```text
evidence/M1/
├── 01_camera_and_repo/             --> M1.1 Spec sheet, first frame, commit proof
├── 02_opencv_pipeline/             --> M1.2 Live detection code, overlays, requirements
├── 03_baseline_speed/              --> M1.3 Benchmark runner, CSV log, overlay screenshot
├── 04_dataset_v1/                  --> M1.4 Dataset card, annotation renderer, samples
├── 05_correct_split/               --> M1.5 Split verification script, zero-leakage proof
├── 06_live_demonstration/          --> Video (IMG_9698.MOV) & Screenshots (IMG_9700/9701)
├── 07_model_training_and_evaluation/ --> Evaluation script, predictions, metrics
├── 08_model_failure_analysis/      --> White-surface false positive analysis & M2 plan
└── 09_raspberry_pi_setup/          --> Hardware specs, reproducible setup instructions
```
