#!/usr/bin/env python3
"""
M2.3: Accuracy Evaluation Script
Compares detection performance (FP32 vs INT8) across the exact same held-out test split.

Author: Mithra Ravi
Milestone: M2 Optimize
"""

from pathlib import Path
from ultralytics import YOLO

def evaluate_accuracy():
    test_dir = Path("data/test/images")
    test_imgs = sorted(list(test_dir.glob("*.jpg")))
    print(f"[*] Running Accuracy Check on {len(test_imgs)} test images...")

    model_pt = YOLO("models/best.pt")
    model_onnx = YOLO("models/best.onnx", task="detect")
    model_int8 = YOLO("models/best_int8.onnx", task="detect")

    print("\n" + "="*80)
    print(f"{'Image Name':<40} | {'PyTorch FP32':<12} | {'ONNX FP32':<12} | {'ONNX INT8':<12}")
    print("="*80)

    for p in test_imgs:
        r_pt = model_pt.predict(str(p), verbose=False)[0]
        r_onnx = model_onnx.predict(str(p), verbose=False)[0]
        r_int8 = model_int8.predict(str(p), verbose=False)[0]

        pt_str = f"{len(r_pt.boxes)} boxes"
        onnx_str = f"{len(r_onnx.boxes)} boxes"
        int8_str = f"{len(r_int8.boxes)} boxes"

        print(f"{p.name[:38]:<40} | {pt_str:<12} | {onnx_str:<12} | {int8_str:<12}")

    print("="*80)
    print("[*] Accuracy check completed successfully!")

if __name__ == "__main__":
    evaluate_accuracy()
