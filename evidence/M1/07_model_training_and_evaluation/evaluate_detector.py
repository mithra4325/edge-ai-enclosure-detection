#!/usr/bin/env python3
"""
M1.6: Model Evaluation and Inference Verification Script
Evaluates the fine-tuned YOLO Nano model (models/best.pt) on test images
and reports detection metrics, confidence scores, and bounding boxes.

Author: Mithra Ravi
Milestone: M1 Detect
"""

import sys
import time
from pathlib import Path
import cv2
from ultralytics import YOLO

def evaluate_model(model_path: str = "models/best.pt", test_dir: str = "data/test/images", conf_thresh: float = 0.25):
    weights = Path(model_path).resolve()
    if not weights.exists():
        raise FileNotFoundError(f"Model file not found: {weights}")

    print("=" * 70)
    print(" ENCLOSURE DETECTOR EVALUATION & VERIFICATION ")
    print("=" * 70)
    print(f"[*] Model Weights:  {weights}")
    print(f"[*] Test Directory: {test_dir}")
    print(f"[*] Conf Threshold: {conf_thresh}")
    print("=" * 70)

    model = YOLO(str(weights))
    print(f"[*] Model loaded successfully. Class names: {model.names}")

    test_path = Path(test_dir)
    images = sorted(list(test_path.glob("*.jpg")))
    print(f"[*] Found {len(images)} test image(s)...")

    total_detections = 0
    for idx, img_path in enumerate(images, start=1):
        t0 = time.perf_counter()
        results = model.predict(source=str(img_path), conf=conf_thresh, verbose=False)
        latency_ms = (time.perf_counter() - t0) * 1000.0

        res = results[0]
        n_boxes = len(res.boxes)
        total_detections += n_boxes

        print(f"\n[{idx}/{len(images)}] {img_path.name}")
        print(f"    - Detections Found: {n_boxes}")
        print(f"    - Inference Time:   {latency_ms:.1f} ms")

        for b_idx, box in enumerate(res.boxes, start=1):
            cls_id = int(box.cls[0].item())
            conf = float(box.conf[0].item())
            xyxy = [round(v, 1) for v in box.xyxy[0].tolist()]
            cls_name = model.names.get(cls_id, "enclosure")
            print(f"      Box {b_idx}: Class '{cls_name}' | Conf: {conf*100:.1f}% | Coordinates: {xyxy}")

    print("\n" + "=" * 70)
    print(f"[*] Total test enclosures detected: {total_detections}")
    print("=" * 70)

if __name__ == "__main__":
    evaluate_model()
