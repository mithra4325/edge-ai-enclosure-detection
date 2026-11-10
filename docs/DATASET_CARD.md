# Dataset Card: 3D-Printed Enclosure Detection v1

**Dataset Name:** `enclosure detector`  
**Roboflow Workspace:** `mithu-1vntk`  
**Roboflow Project ID:** `object-detection-n6b60`  
**Web URL:** [https://universe.roboflow.com/mithu-1vntk/object-detection-n6b60](https://universe.roboflow.com/mithu-1vntk/object-detection-n6b60)  
**Version:** Version 1 (`2026-11-10 2:37pm`)  
**License:** Creative Commons Attribution 4.0 International (CC BY 4.0)  
**Author / Collector:** Mithra Ravi (`mithra4325`)  

---

## 1. Dataset Overview

The **Enclosure Detection Dataset v1** is an authentic, physical computer vision dataset curated to train edge AI detectors to recognize a custom **3D-printed PIR sensor camera enclosure** designed in CAD ([`cad/pir_sensor_enclosure_mithra_ravi.stl`](../cad/pir_sensor_enclosure_mithra_ravi.stl)).

All 40 photographs depict the physical 3D-printed artifact under varied angles and lighting. Bounding boxes were manually drawn using Roboflow Annotation Studio.

- **Target Object Class:** `enclosure` (Class ID `0`)
- **Number of Classes:** 1 (Single-class detection)
- **Total Images:** 40 authentic captures
- **Total Annotations:** 60 bounding boxes
- **Average Objects Per Image:** 1.5 enclosures/image
- **Native Resolution:** $4032 \times 3024$ and $3024 \times 4032$ (high-resolution smartphone CMOS sensor)

---

## 2. Partition Splits & Zero Data Leakage

The dataset strictly conforms to the standard academic **70% / 20% / 10%** distribution:

| Partition | Image Count | Percentage | Bounding Box Annotations | Storage Directory in Repository |
| :--- | :---: | :---: | :---: | :--- |
| **Training Set** | **28** | **70.0%** | 44 | [`data/train/`](../data/train/) |
| **Validation Set** | **8** | **20.0%** | 11 | [`data/valid/`](../data/valid/) |
| **Held-Out Test Set** | **4** | **10.0%** | 5 | [`data/test/`](../data/test/) |
| **Total** | **40** | **100.0%** | **60** | [`data/`](../data/) |

### Leakage Verification
- **Automated Verification Script:** [`correct_split/verify_split.py`](../correct_split/verify_split.py)
- **Audit Methodology:** 256-bit SHA-256 cryptographic hash computation across all image binaries.
- **Filename Overlap:** **0** across all pair combinations.
- **Hash Collisions:** **0** across all pair combinations.
- **Verification Verdict:** **SUCCESS — ZERO DATA LEAKAGE CONFIRMED** ([`correct_split/verification_results.txt`](../correct_split/verification_results.txt)).

---

## 3. Annotation Specifications

Annotations follow the standard normalized Darknet / YOLO format:
```text
<class_id> <x_center> <y_center> <width> <height>
```
Where all spatial coordinates are floating-point values normalized to $[0.0, 1.0]$ relative to image dimensions.

- **Tightness Standard:** Bounding boxes enclose outer mechanical edges (mounting tabs, chamfered corners, lens dome) with minimal background margin.
- **Visually Annotated Copies:** All 40 images with rendered bounding boxes, corner anchors, and Roboflow magenta badges are archived in [`dataset_v1/annotated_images/`](../dataset_v1/annotated_images/).

---

## 4. Preprocessing & Augmentation Pipeline

- **Auto-Orientation:** EXIF orientation flags were automatically applied and stripped during Roboflow export to ensure consistent matrix indexing.
- **Synthetic Augmentation:** None applied during v1 export. All images represent genuine physical camera acquisitions.

---

## 5. Dataset Limitations & Known Background Bias

1. **Background Homogeneity (The Dark Workbench Bias):**
   - *Observation:* All 40 images were photographed against a dark brown wooden workbench.
   - *Consequence:* The white enclosure exhibits intense luminance contrast against the dark background. The model learned to correlate high-contrast white boundaries with enclosure presence, inducing false positives on light-colored walls and white papers in real-world environments.
2. **Absence of Hard-Negative Samples:**
   - Every image in Dataset v1 contains at least one enclosure (positive sample).
   - Zero images without enclosures were included. The loss function was never exposed to negative examples of white non-enclosure objects (white paper, white boxes, pale desks) with empty annotations.
3. **M2 Dataset Roadmap:**
   - Collect 60+ images on light desks, metallic benches, and outdoor environments.
   - Inject 20+ hard-negative images containing non-enclosure white objects labeled with zero bounding boxes.
