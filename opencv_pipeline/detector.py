"""
Edge AI Enclosure Detector Module
Loads the original trained YOLO Nano model and performs real-time inference on Raspberry Pi 5.
"""

import time
from pathlib import Path
from typing import List, Dict, Any, Tuple
import cv2
import numpy as np
from ultralytics import YOLO


class EnclosureDetector:
    """Trained YOLO Nano Object Detector for 3D-Printed Enclosures."""

    def __init__(self, model_path: str = "models/best.pt", conf_thresh: float = 0.25, imgsz: int = 640):
        self.model_path = Path(model_path).resolve()
        if not self.model_path.exists():
            raise FileNotFoundError(f"Original trained model weights not found at: {self.model_path}")

        print(f"[*] Initializing EnclosureDetector with model: {self.model_path}")
        self.model = YOLO(str(self.model_path), task="detect")
        self.names = self.model.names or {0: "enclosure"}
        self.conf_thresh = conf_thresh
        self.imgsz = imgsz
        print(f"[*] Model loaded successfully. Class names: {self.names}")

    def detect(self, frame: np.ndarray) -> Tuple[List[Dict[str, Any]], float]:
        """
        Runs object detection on a BGR image frame.
        Returns:
            detections: List of dicts with keys: bbox, confidence, class_id, class_name
            inference_ms: Inference time in milliseconds
        """
        t0 = time.perf_counter()
        results = self.model.predict(
            source=frame,
            conf=self.conf_thresh,
            imgsz=self.imgsz,
            device="cpu",
            verbose=False
        )
        inference_ms = (time.perf_counter() - t0) * 1000.0

        detections = []
        result = results[0]
        if result.boxes is not None and len(result.boxes) > 0:
            for box in result.boxes:
                cls_id = int(box.cls[0].item())
                conf = float(box.conf[0].item())
                xyxy = [int(v) for v in box.xyxy[0].tolist()]
                detections.append({
                    "bbox": xyxy,
                    "confidence": conf,
                    "class_id": cls_id,
                    "class_name": self.names.get(cls_id, "enclosure")
                })

        return detections, inference_ms

    def annotate_frame(
        self,
        frame: np.ndarray,
        detections: List[Dict[str, Any]],
        fps: float,
        latency_ms: float,
        system_stats: Dict[str, Any]
    ) -> np.ndarray:
        """
        Draws high-contrast bounding boxes and clean HUD telemetry overlay on the frame.
        """
        annotated = frame.copy()
        h, w = annotated.shape[:2]

        # 1. Draw Bounding Boxes for detected enclosures
        for det in detections:
            x1, y1, x2, y2 = det["bbox"]
            conf = det["confidence"]
            label = f"{det['class_name']}: {conf * 100:.1f}%"

            # Bounding box (neon green: BGR 0, 255, 128)
            cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 255, 128), 2)

            # Label badge
            (lbl_w, lbl_h), baseline = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.55, 2)
            lbl_y1 = max(y1 - lbl_h - 10, 0)
            lbl_y2 = lbl_y1 + lbl_h + 8
            lbl_x2 = min(x1 + lbl_w + 10, w)

            cv2.rectangle(annotated, (x1, lbl_y1), (lbl_x2, lbl_y2), (0, 255, 128), -1)
            cv2.putText(
                annotated,
                label,
                (x1 + 5, lbl_y2 - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (0, 0, 0),
                2,
                cv2.LINE_AA
            )

        # 2. Semi-transparent HUD Header Banner at top
        banner_h = 105
        overlay = annotated.copy()
        cv2.rectangle(overlay, (0, 0), (w, banner_h), (20, 20, 20), -1)
        cv2.addWeighted(overlay, 0.75, annotated, 0.25, 0, annotated)

        # 3. HUD Text Overlay
        # Line 1: Title & Target
        cv2.putText(
            annotated,
            "ENCLOSURE DETECTION",
            (15, 24),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (0, 255, 255),
            2,
            cv2.LINE_AA
        )

        obj_count = len(detections)
        status_color = (0, 255, 128) if obj_count > 0 else (180, 180, 180)
        cv2.putText(
            annotated,
            f"Objects detected: {obj_count}",
            (15, 52),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            status_color,
            2,
            cv2.LINE_AA
        )

        # Line 2: Performance Telemetry
        telemetry_str = f"FPS: {fps:.1f}   |   Inference latency: {latency_ms:.1f} ms"
        cv2.putText(
            annotated,
            telemetry_str,
            (15, 76),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (255, 255, 255),
            1,
            cv2.LINE_AA
        )

        # Line 3: System Status (CPU / Temp / RAM)
        sys_str = (
            f"CPU: {system_stats.get('cpu_percent', 0.0)}%   |   "
            f"Temp: {system_stats.get('cpu_temp_c', 0.0)}C   |   "
            f"RAM: {system_stats.get('ram_used_mb', 0.0)}MB (CPU Inference)"
        )
        cv2.putText(
            annotated,
            sys_str,
            (15, 96),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.45,
            (200, 200, 200),
            1,
            cv2.LINE_AA
        )

        return annotated
