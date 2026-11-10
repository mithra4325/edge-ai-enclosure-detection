#!/usr/bin/env python3
"""
M2.2: Dynamic INT8 Model Quantization Script
Converts FP32 ONNX model into an optimized INT8 model using onnxruntime.quantization.

Author: Mithra Ravi
Milestone: M2 Optimize
"""

import os
from pathlib import Path
import onnxruntime.quantization as ort_quant

def quantize_model(input_onnx: str = "models/best.onnx", output_onnx: str = "models/best_int8.onnx"):
    in_path = Path(input_onnx).resolve()
    out_path = Path(output_onnx).resolve()

    if not in_path.exists():
        raise FileNotFoundError(f"Source ONNX model not found: {in_path}")

    print(f"[*] Starting dynamic INT8 quantization: {in_path.name} -> {out_path.name}")
    ort_quant.quantize_dynamic(
        model_input=str(in_path),
        model_output=str(out_path),
        weight_type=ort_quant.QuantType.QUInt8
    )

    size_orig = os.path.getsize(in_path) / (1024 * 1024)
    size_quant = os.path.getsize(out_path) / (1024 * 1024)
    reduction = ((size_orig - size_quant) / size_orig) * 100.0

    print(f"[*] Quantization complete!")
    print(f"    - Original Size (FP32): {size_orig:.2f} MB")
    print(f"    - Quantized Size (INT8): {size_quant:.2f} MB")
    print(f"    - Storage Reduction:     {reduction:.1f}%")

if __name__ == "__main__":
    quantize_model()
