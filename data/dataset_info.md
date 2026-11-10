# Enclosure Detection Dataset

This dataset was created and annotated on **Roboflow** for the 3D-Printed Camera Enclosure Detection project.

## Dataset Specifications

- **Project Name:** `enclosure detector` (`object-detection-n6b60`)
- **Workspace:** `mithu-1vntk`
- **Roboflow Universe URL:** [https://universe.roboflow.com/mithu-1vntk/object-detection-n6b60](https://universe.roboflow.com/mithu-1vntk/object-detection-n6b60)
- **Version:** Version 1 (`2026-11-10 2:37pm`)
- **License:** Creative Commons Attribution 4.0 International (CC BY 4.0)
- **Target Class:** `enclosure` (Class ID `0`)
- **Annotation Format:** YOLO format (`class x_center y_center width height` normalized $[0, 1]$)
- **Preprocessing:** Auto-orientation of pixel data (EXIF-orientation stripping)
- **Image Augmentation:** None applied in export

## Split Distribution

| Split | Images | Target Bounding Boxes | Percentage |
| :--- | :---: | :---: | :---: |
| **Train** | 28 | 44 | 70% |
| **Validation** | 8 | 11 | 20% |
| **Test (Held-Out)** | 4 | 5 | 10% |
| **Total** | **40** | **60** | **100%** |

## Directory Structure

```
data/
├── data.yaml           # Portable YOLO dataset manifest
├── samples/            # Held-out samples for quick evaluation
├── train/
│   ├── images/
│   └── labels/
├── valid/
│   ├── images/
│   └── labels/
└── test/
    ├── images/
    └── labels/
```
