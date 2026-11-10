#!/usr/bin/env python3
"""
M2.2: Live INT8 Enclosure Detection Runner
Executes live inference using the quantized INT8 ONNX model on Raspberry Pi 5.

Author: Mithra Ravi
Milestone: M2 Optimize
"""

import sys
import time
from pathlib import Path
import cv2
from ultralytics import YOLO

def run_live_int8(model_path: str = "models/best_int8.onnx", camera_index: int = 0):
    model_file = Path(model_path).resolve()
    if not model_file.exists():
        raise FileNotFoundError(f"INT8 model not found at: {model_file}")

    print(f"[*] Loading Quantized INT8 Model: {model_file}")
    model = YOLO(str(model_file), task="detect")

    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print(f"[!] Camera index {camera_index} not accessible.")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    print("[*] Streaming INT8 detections. Press 'q' to quit.")
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            t0 = time.perf_counter()
            results = model.predict(source=frame, conf=0.25, verbose=False)
            latency_ms = (time.perf_counter() - t0) * 1000.0

            res = results[0]
            annotated = res.plot()
            cv2.putText(annotated, f"INT8 ONNX | Latency: {latency_ms:.1f}ms", (20, 35),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 255), 2)
            cv2.imshow("INT8 Quantized Detection", annotated)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    run_live_int8()
