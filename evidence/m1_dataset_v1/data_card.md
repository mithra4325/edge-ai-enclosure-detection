# M1.4: Dataset v1 Data Card & Annotation Quality

**Student Name:** Mithra Ravi  
**Milestone:** M1 Detect  
**Task:** Dataset v1 (Max marks: 4)  
**Proof Statement:** *"I label images with tight, correct boxes. I show my own labelled images and the data card"*

---

## 1. Dataset Card Summary

| Attribute | Specification |
| :--- | :--- |
| **Dataset Title** | Custom 3D-Printed Sensor Enclosure Dataset v1 |
| **Roboflow Workspace** | `mithu-1vntk` |
| **Roboflow Project** | `object-detection-n6b60` (`enclosure detector`) |
| **Public Dataset URL** | [https://universe.roboflow.com/mithu-1vntk/object-detection-n6b60](https://universe.roboflow.com/mithu-1vntk/object-detection-n6b60) |
| **Target Object** | Custom 3D-Printed PIR Sensor Enclosure (Designed in CAD, sliced, and printed in PLA) |
| **Class Label** | `enclosure` (Single-class object detector, Class ID: `0`) |
| **Total Images** | 40 real-world captures |
| **Total Annotations** | 60 bounding boxes |
| **Annotation Tool** | Roboflow Web Annotation Suite |
| **Annotation Format** | YOLO format (`class_id x_center y_center width height` normalized to $[0, 1]$) |
| **License** | Creative Commons Attribution 4.0 International (CC BY 4.0) |

---

## 2. Tight Bounding Box Labeling Standards

To achieve high detection accuracy and avoid background noise overfitting, the following labeling protocol was strictly enforced:

1. **Tight Boundary Fit:** The bounding box edges touch the outermost geometric perimeter of the 3D-printed enclosure (including mounting tabs and sensor lens openings) without unnecessary background margin.
2. **Occlusion Handling:** When the enclosure is partially occluded by a hand, mounting bracket, or test surface, the box encompasses only the visible extents of the enclosure body.
3. **Orientation Invariance:** Captured across multiple 3D spatial rotations: front-facing, back opening, side profile, top-down, and oblique angles ($45^\circ$).
4. **Lighting Diversity:** Photographed under direct overhead LED lighting, diffuse ambient daylight, angled spotlights, and low-light shadow conditions to prevent lighting bias.
5. **No Negative Label Noise:** Zero false background labels; ambiguous reflections were strictly excluded.

---

## 3. Labeled Sample Image Evidence

Below are representative training set images with their tight ground-truth annotations rendered:

| Sample | Filename | Ground-Truth Labels | Key Challenge Addressed |
| :---: | :--- | :---: | :--- |
| **1** | [`tight_labeled_sample_1.jpg`](tight_labeled_sample_1.jpg) | 1 tight box | High-contrast workbench background with edge alignment |
| **2** | [`tight_labeled_sample_2.jpg`](tight_labeled_sample_2.jpg) | 1 tight box | Close-up macro perspective with shallow depth-of-field |
| **3** | [`tight_labeled_sample_3.jpg`](tight_labeled_sample_3.jpg) | 1 tight box | Angled oblique orientation showing 3D layer lines |
| **4** | [`tight_labeled_sample_4.jpg`](tight_labeled_sample_4.jpg) | 1 tight box | Multi-object spatial relationship in field of view |

---

## 4. Dataset Preprocessing

- **EXIF Auto-Orientation:** Pixel data auto-oriented to strip mobile device rotation metadata.
- **Resolution:** Captured in high-resolution ($3024 \times 4032$ / $1280 \times 720$) and scaled dynamically to $640 \times 640$ with auto-letterbox preservation during model inference.
- **Zero Augmentation in Raw Data:** Ground-truth labels reflect physical, authentic photographs of the enclosure without synthetic distortion artifacts.
