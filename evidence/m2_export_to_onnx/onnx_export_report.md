# M2.1: ONNX Model Export & Verification Report

**Student Name:** Mithra Ravi  
**Milestone:** M2 Optimize  
**Task:** Export to ONNX (Max marks: 3)  
**Proof Statement:** *"I run the ONNX export myself and show my commit"*

---

## 1. Export Overview

The trained YOLO Nano PyTorch model (`models/best.pt`) was exported to **Open Neural Network Exchange (ONNX)** format to enable hardware-independent edge inference with `onnxruntime`.

- **Source PyTorch Model:** `models/best.pt` (5.16 MB)
- **Target ONNX Model:** `models/best.onnx` (9.34 MB)
- **ONNX Opset Version:** **Opset 17**
- **Simplifier:** ONNX-Simplifier applied (fused Conv + BatchNorm layers)
- **Input Tensor Signature:** `images: [1, 3, 640, 640]` (Float32, RGB, $[0.0, 1.0]$)
- **Output Tensor Signature:** `output0: [1, 5, 8400]` (Float32: 4 box coordinates + 1 class probability)

---

## 2. Graph & Signature Verification

The exported model graph was validated using Python `onnxruntime`:

```python
import onnxruntime as ort

session = ort.InferenceSession("models/best.onnx")
inputs = session.get_inputs()
outputs = session.get_outputs()

print(f"Input Name:  {inputs[0].name}  | Shape: {inputs[0].shape} | Type: {inputs[0].type}")
print(f"Output Name: {outputs[0].name} | Shape: {outputs[0].shape} | Type: {outputs[0].type}")
```

**Output:**
```
Input Name:  images  | Shape: [1, 3, 640, 640] | Type: tensor(float)
Output Name: output0 | Shape: [1, 5, 8400]     | Type: tensor(float)
```

---

## 3. Benefits for Raspberry Pi 5 Deployment

1. **Framework Decoupling:** ONNX models run directly using `onnxruntime` without requiring the heavyweight PyTorch training framework.
2. **CPU Execution Provider:** Leverages the high-performance Microsoft ONNX Runtime `CPUExecutionProvider` compiled with ARM NEON SIMD vector acceleration.
3. **Reproducible Script:** Export can be reproduced at any time using [`export_onnx.py`](export_onnx.py).
4. **Git Commit Reference:** Export script and verified ONNX artifact committed directly in repository history.
