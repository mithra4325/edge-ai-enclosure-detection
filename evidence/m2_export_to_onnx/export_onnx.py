#!/usr/bin/env python3
"""
M2.1: ONNX Model Export Script
Exports fine-tuned YOLO Nano PyTorch weights to portable ONNX format (Opset 17).

Author: Mithra Ravi
Milestone: M2 Optimize
"""

import sys
import os
from pathlib import Path
from ultralytics import YOLO

def export_model(weights_path: str = "models/best.pt", opset: int = 17, imgsz: int = 640):
    weights = Path(weights_path).resolve()
    if not weights.exists():
        raise FileNotFoundError(f"PyTorch weights not found at: {weights}")

    print(f"[*] Loading PyTorch model from: {weights}")
    model = YOLO(str(weights))

    print(f"[*] Exporting to ONNX format (opset={opset}, imgsz={imgsz})...")
    output_path = model.export(
        format="onnx",
        opset=opset,
        imgsz=imgsz,
        dynamic=False,
        simplify=True
    )
    print(f"[*] Export successful! ONNX model located at: {output_path}")
    print(f"[*] File size: {os.path.getsize(output_path) / (1024 * 1024):.2f} MB")
    return output_path

if __name__ == "__main__":
    export_model()
