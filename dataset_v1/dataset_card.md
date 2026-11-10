# Dataset Card: 3D-Printed Camera Enclosure Detection v1

**Dataset Name:** `enclosure detector`  
**Dataset Workspace:** `mithu-1vntk`  
**Roboflow Project ID:** `object-detection-n6b60`  
**Roboflow URL:** [https://universe.roboflow.com/mithu-1vntk/object-detection-n6b60](https://universe.roboflow.com/mithu-1vntk/object-detection-n6b60)  
**Version:** Version 1 (`2026-11-10 2:37pm`)  
**License:** Creative Commons Attribution 4.0 International (CC BY 4.0)  
**Author / Annotator:** Mithra Ravi (`mithra4325`)  

---

## 1. Dataset Summary

This dataset consists of **40 high-resolution physical photographs** capturing a custom **3D-printed PIR sensor camera enclosure** designed in CAD (`cad/pir_sensor_enclosure_mithra_ravi.stl`), sliced, and printed using black PLA filament. The dataset was collected, uploaded, and annotated using the Roboflow computer vision annotation platform.

- **Primary Object Class:** `enclosure` (Class ID `0`)
- **Number of Classes:** 1 (Single-class object detection)
- **Total Images:** 40
- **Total Labeled Enclosures:** 60 bounding boxes
- **Average Targets Per Image:** 1.5 enclosures/image

---

## 2. Dataset Structure and Splits

The dataset follows an exact **70% / 20% / 10%** split ratio:

| Split Partition | Images | Percentage | Bounding Box Annotations | Storage Directory in Repository |
| :--- | :---: | :---: | :---: | :--- |
| **Training Split** | **28** | **70.0%** | 44 | [`data/train/`](../data/train/) |
| **Validation Split** | **8** | **20.0%** | 11 | [`data/valid/`](../data/valid/) |
| **Testing Split (Held-Out)** | **4** | **10.0%** | 5 | [`data/test/`](../data/test/) |
| **Total** | **40** | **100.0%** | **60** | [`data/`](../data/) |

---

## 3. Annotation Methodology & Quality Standards

- **Tool:** Roboflow Web Annotation Studio.
- **Bounding Box Tightness:** Boxes fit snugly along outer mechanical edges (screw tabs, sensor lens dome, cable cutouts) without unnecessary background margins.
- **Occlusion Handling:** Only visible surfaces are enclosed when parts are partially occluded by fixtures or hands.
- **Lighting Variation:** Images were captured under varied conditions: overhead fluorescent light, natural daylight, oblique desk lamps, and shadowed desk corners.
- **Perspective Diversity:** Captured at distances between 0.15m and 1.5m across $0^\circ$ (face-on), $45^\circ$ (oblique), $90^\circ$ (profile), and inverted configurations.
- **Format:** Normalized YOLO format:
  ```text
  <class_id> <x_center> <y_center> <width> <height>
  ```
  Where coordinates are floating-point values normalized to $[0.0, 1.0]$.
