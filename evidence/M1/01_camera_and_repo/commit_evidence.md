# Git Repository & Commit Evidence

**Project Title:** Edge AI 3D-Printed Enclosure Detection  
**Author / Student:** Mithra Ravi (`mithra4325`)  
**Assessment Milestone:** M1.1 — Camera and Repository  

---

## 1. Repository Details

- **GitHub Repository:** [https://github.com/mithra4325/edge-ai-enclosure-detection](https://github.com/mithra4325/edge-ai-enclosure-detection)
- **GitHub Username:** `mithra4325`
- **Default Branch:** `main`
- **Remote URL:** `https://github.com/mithra4325/edge-ai-enclosure-detection.git`

---

## 2. Commit Log Evidence

The project deployment work and camera setup are tracked by individual commits on `main`:

```text
commit 556ff115fb0af51ebe8a8d398c5986faccec0b7b
Author: mithra4325 <mithraravi76@gmail.com>
Date:   Tue Nov 10 16:00:41 2026 +0530

    Deploy edge AI enclosure detection pipeline on Raspberry Pi 5 (M1 Milestone)
    
    - Add low-latency threaded camera capture module (src/camera.py)
    - Add YOLO Nano enclosure detector with HUD telemetry overlay (src/detector.py)
    - Add system hardware telemetry monitor and benchmark CSV logger (src/monitor.py)
    - Add single-command launch script (run_detection.sh)
    - Collect and organize physical assessment evidence for M1.1, M1.2, and M1.3
    - Document hardware specs, baseline results (3.5 FPS, 280ms CPU latency), and run instructions in README.md
```

---

## 3. Preservation of Original Model Integrity

The original trained weights and dataset configurations were preserved with zero modification:
- `models/best.pt` (Original PyTorch weights from Roboflow training)
- `models/best.onnx` (Original ONNX export)
- `models/model_metadata.json` (Original training metrics)
- `data/data.yaml` (Original dataset split definition)
