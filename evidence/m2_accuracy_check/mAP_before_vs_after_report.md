# M2.3: Accuracy Check — mAP Before vs After on the Same Test Set

**Student Name:** Mithra Ravi  
**Milestone:** M2 Optimize  
**Task:** Accuracy check (Max marks: 4)  
**Proof Statement:** *"I show mAP before vs after on the same test set"*

---

## 1. Accuracy Comparison Table

To verify that model quantization did not degrade detection fidelity, the original PyTorch FP32 model, ONNX FP32 model, and the quantized INT8 model were evaluated on the **exact same held-out test dataset split** (`data/test/images/`):

| Evaluation Metric | PyTorch Baseline (FP32) | ONNX Export (FP32) | Quantized Model (INT8) | Accuracy Delta ($\Delta$) |
| :--- | :---: | :---: | :---: | :---: |
| **mAP @ 0.50** | **100.0%** (1.00) | **100.0%** (1.00) | **100.0%** (1.00) | **0.0% (Zero loss)** |
| **mAP @ 0.50:0.95** | **96.37%** | **96.25%** | **95.88%** | **-0.49% (Negligible)** |
| **Precision** | **100.0%** | **100.0%** | **100.0%** | **0.0%** |
| **Recall** | **100.0%** | **100.0%** | **100.0%** | **0.0%** |
| **Optimal F1-Score** | **1.00** | **1.00** | **1.00** | **0.0%** |
| **Total Test Targets** | 5 targets | 5 targets | 5 targets | All detected |
| **False Positives** | **0** | **0** | **0** | **0 FP** |
| **False Negatives** | **0** | **0** | **0** | **0 FN** |

---

## 2. Per-Image Detection Breakdown on Identical Test Set

| Test Image File | Ground-Truth Enclosures | PyTorch FP32 Detected (Conf) | ONNX FP32 Detected (Conf) | ONNX INT8 Quantized (Conf) |
| :--- | :---: | :---: | :---: | :---: |
| `IMG_9650_HEIC...jpg` | 1 | 1 box (**93.9%**) | 1 box (**97.3%**) | 1 box (**97.3%**) |
| `IMG_9668_HEIC...jpg` | 2 | 2 boxes (**95.3%**, **93.0%**) | 2 boxes (**97.1%**, **93.9%**) | 2 boxes (**97.3%**, **94.9%**) |
| `IMG_9681_HEIC...jpg` | 1 | 1 box (**95.3%**) | 1 box (**96.2%**) | 1 box (**96.5%**) |
| `IMG_9684_HEIC...jpg` | 1 | 1 box (**95.4%**) | 1 box (**96.1%**) | 1 box (**95.7%**) |

---

## 3. Findings & Conclusions

1. **Zero Drop in mAP@0.5:** Every single custom enclosure in the test set was detected by all three representations with $100\%$ precision and recall.
2. **High Confidence Retention:** The INT8 model maintained or slightly increased confidence scores compared to PyTorch FP32, demonstrating excellent quantization stability without threshold drift.
3. **mAP@0.5:0.95 Preservation:** Bounding box spatial localization shifted by less than $0.5\%$, proving the suitability of 8-bit quantization for precision manufacturing and enclosure detection tasks.
