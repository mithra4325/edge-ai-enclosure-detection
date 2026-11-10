#!/usr/bin/env python3
"""
Portable Object Detection Inference Script
Model: YOLO Nano (YOLO26n) trained for 3D-Printed Enclosure Detection
Author: Mithra Ravi (mithra4325)
Project: edge-ai-enclosure-detection
"""

import argparse
import os
import sys
import time
from pathlib import Path
import cv2
import numpy as np


def run_inference(model_path: str, source: str, conf_thresh: float = 0.25, iou_thresh: float = 0.45, save_dir: str = "runs/detect", show: bool = False):
    """
    Run object detection using the fine-tuned YOLO model.
    Supports both PyTorch (.pt) and ONNX (.onnx) formats.
    """
    from ultralytics import YOLO

    model_path = Path(model_path).resolve()
    if not model_path.exists():
        raise FileNotFoundError(f"Model file not found at: {model_path}")

    print(f"[*] Loading model from: {model_path}")
    model = YOLO(str(model_path), task="detect")
    names = model.names or {0: "enclosure"}
    print(f"[*] Model loaded successfully. Class names: {names}")

    # Check source type (webcam vs file/folder)
    is_cam = source.isdigit() or source.startswith("/dev/video")
    src = int(source) if source.isdigit() else source

    save_path = Path(save_dir)
    save_path.mkdir(parents=True, exist_ok=True)

    if is_cam:
        print(f"[*] Opening camera stream on device index: {src}")
        cap = cv2.VideoCapture(src)
        if not cap.isOpened():
            print(f"[!] Error: Could not open camera device {src}")
            return

        print("[*] Streaming live inference. Press 'q' in video window to exit.")
        frame_idx = 0
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    print("[!] Failed to grab frame from camera.")
                    break

                t0 = time.time()
                results = model.predict(source=frame, conf=conf_thresh, iou=iou_thresh, verbose=False)
                latency_ms = (time.time() - t0) * 1000.0

                result = results[0]
                annotated = result.plot()
                enclosure_count = len(result.boxes)

                # Draw telemetry banner on frame
                hud_text = f"Enclosures: {enclosure_count} | Latency: {latency_ms:.1f}ms ({1000.0/max(latency_ms, 1e-5):.1f} FPS)"
                cv2.putText(annotated, hud_text, (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

                if show:
                    cv2.imshow("Edge AI Enclosure Detector", annotated)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

                frame_idx += 1
        finally:
            cap.release()
            cv2.destroyAllWindows()
            print(f"[*] Camera session finished. Total frames processed: {frame_idx}")
    else:
        source_path = Path(source)
        if not source_path.exists():
            raise FileNotFoundError(f"Source path not found: {source_path}")

        image_files = []
        if source_path.is_file():
            image_files.append(source_path)
        else:
            valid_exts = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
            image_files = [p for p in source_path.iterdir() if p.suffix.lower() in valid_exts]

        print(f"[*] Running inference on {len(image_files)} image(s)...")

        total_detections = 0
        for idx, img_path in enumerate(image_files, start=1):
            t0 = time.time()
            results = model.predict(source=str(img_path), conf=conf_thresh, iou=iou_thresh, verbose=False)
            latency_ms = (time.time() - t0) * 1000.0

            result = results[0]
            boxes = result.boxes
            num_boxes = len(boxes)
            total_detections += num_boxes

            print(f"[{idx}/{len(image_files)}] {img_path.name}: {num_boxes} enclosure(s) found (Latency: {latency_ms:.1f}ms)")
            for i, box in enumerate(boxes):
                cls_id = int(box.cls[0].item())
                conf = float(box.conf[0].item())
                xyxy = [round(v, 1) for v in box.xyxy[0].tolist()]
                cls_name = names.get(cls_id, str(cls_id))
                print(f"    - Detection {i+1}: Class '{cls_name}' | Confidence: {conf:.2%} | Box [x1, y1, x2, y2]: {xyxy}")

            out_file = save_path / f"pred_{img_path.name}"
            result.save(filename=str(out_file))

        print(f"[*] Inference complete! Total detections: {total_detections}")
        print(f"[*] Annotated results saved to: {save_path.resolve()}")


def main():
    parser = argparse.ArgumentParser(description="Edge AI Enclosure Detection Inference Engine")
    parser.add_argument("--model", type=str, default="models/best.pt", help="Path to weights file (.pt or .onnx)")
    parser.add_argument("--source", type=str, default="data/samples", help="Path to image, directory, or camera index (0)")
    parser.add_argument("--conf", type=float, default=0.25, help="Confidence threshold (default: 0.25)")
    parser.add_argument("--iou", type=float, default=0.45, help="NMS IoU threshold (default: 0.45)")
    parser.add_argument("--save-dir", type=str, default="runs/detect", help="Output directory for annotated results")
    parser.add_argument("--show", action="store_true", help="Display live OpenCV window during streaming")
    args = parser.parse_args()

    run_inference(
        model_path=args.model,
        source=args.source,
        conf_thresh=args.conf,
        iou_thresh=args.iou,
        save_dir=args.save_dir,
        show=args.show
    )


if __name__ == "__main__":
    main()
