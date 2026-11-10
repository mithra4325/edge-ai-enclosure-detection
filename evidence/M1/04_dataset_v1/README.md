# M1.4: Dataset v1 & Data Card Documentation

**Status:** **COMPLETE**

---

## 1. Purpose of the Task
The objective of Milestone 1.4 is to document the authentic, physical computer vision dataset created for the custom 3D-printed enclosure detection task. This includes presenting the formal Dataset Card, detailing image acquisition, specifying annotation format and methodology, providing ground-truth labeled image examples, and recording the dataset's splits and licensing.

## 2. What I Implemented
- Collected 40 photographic images of the physical 3D-printed PIR camera enclosure under diverse angles, workbench backgrounds, and lighting environments.
- Manually annotated 60 individual enclosure instances with tight bounding boxes using the Roboflow platform.
- Exported the dataset into standard YOLO format (`data.yaml` manifest + text label files).
- Created a formal Dataset Card ([`dataset_card.md`](dataset_card.md)) outlining technical attributes, source details, and licensing.
- Rendered visual proof of tight, correct ground-truth bounding boxes on sample images (`annotated_sample_1.jpg` through `annotated_sample_4.jpg`).

## 3. Hardware Used
- **Target Object:** Custom 3D-printed PIR sensor enclosure designed in CAD (`cad/pir_sensor_enclosure_mithra_ravi.stl`), printed on a fused deposition modeling (FDM) 3D printer using black PLA filament.
- **Capture Equipment:** High-resolution digital camera sensor and Logitech C270 HD webcam.
- **Deployment SBC:** Raspberry Pi 5 Model B Rev 1.1.

## 4. Software and Dependencies
- **Annotation Tool:** Roboflow Cloud Computer Vision Annotation Suite.
- **Annotation Format:** YOLO darknet format (`class_id x_center y_center width height` normalized to $[0.0, 1.0]$).
- **Processing Libraries:** Python 3.13, OpenCV 4.10, PyYAML 6.0.

## 5. How the Implementation Works
1. **Physical Object Production:** The CAD file was drafted and exported to STL, then 3D-printed to serve as the physical target object for detection.
2. **Image Acquisition:** 40 authentic photographs were captured covering varied orientations (flat, tilted, side, upside-down) and environmental lighting.
3. **Bounding Box Annotation:** Every enclosure was tightly labeled in Roboflow. The bounding box outlines the outer physical perimeter of the enclosure.
4. **Export & Partitioning:** The dataset was exported into YOLO format and partitioned into training (`data/train/`), validation (`data/valid/`), and held-out test (`data/test/`) splits with an exact 70/20/10 ratio.
5. **Auto-Orientation:** EXIF orientation flags were stripped during export to ensure consistent top-left coordinate alignment across edge inference backends.

## 6. How to Reproduce or Run It
To inspect the dataset labels and render ground-truth bounding boxes on all 40 images on the Raspberry Pi 5:
```bash
# 1. Activate virtual environment
source venv/bin/activate

# 2. Inspect data manifest
cat data/data.yaml

# 3. Generate visually annotated images for all 40 images across train, valid, and test
python dataset_v1/annotate_dataset.py
```

## 7. Evidence Available in this Folder
- [`dataset_card.md`](dataset_card.md): Comprehensive Dataset Card covering specifications, class definitions, and attribution.
- [`annotate_dataset.py`](annotate_dataset.py): Automated script generating visually annotated ground-truth images with Roboflow magenta bounding boxes and badges.
- [`annotated_images/`](annotated_images/): Complete directory of **all 40 visually annotated images** across all splits:
  - [`annotated_images/train/`](annotated_images/train/): All 28 training images with tight ground-truth bounding boxes (44 instances).
  - [`annotated_images/valid/`](annotated_images/valid/): All 8 validation images with tight ground-truth bounding boxes (11 instances).
  - [`annotated_images/test/`](annotated_images/test/): All 4 held-out test images with tight ground-truth bounding boxes (5 instances).
- High-resolution sample previews:
  - [`annotated_sample_1.jpg`](annotated_sample_1.jpg): Ground-truth tight bounding box on workbench background.
  - [`annotated_sample_2.jpg`](annotated_sample_2.jpg): Ground-truth tight bounding box on close-up perspective.
  - [`annotated_sample_3.jpg`](annotated_sample_3.jpg): Ground-truth tight bounding box on oblique angled enclosure.
  - [`annotated_sample_4.jpg`](annotated_sample_4.jpg): Ground-truth tight bounding box on multi-enclosure scene.

## 8. Actual Results

### Dataset Metrics & Breakdown

| Dataset Attribute | Actual Project Value | Status |
| :--- | :--- | :---: |
| **Object Class Name** | `enclosure` (ID: `0`) | Single-Class Detector |
| **Total Images** | **40** authentic captures | Complete |
| **Total Annotations** | **60** bounding boxes | Complete |
| **Training Split** | 28 images (**70.0%**), 44 targets | Complete |
| **Validation Split** | 8 images (**20.0%**), 11 targets | Complete |
| **Testing Split** | 4 images (**10.0%**), 5 targets | Complete |
| **Roboflow Workspace**| `mithu-1vntk` | Publicly Available |
| **Roboflow Project** | `object-detection-n6b60` (`enclosure detector`) | Version 1 Verified |
| **License** | Creative Commons Attribution 4.0 International (CC BY 4.0) | Open Academic Use |

## 9. Pending Items and Limitations
- **Pending Items:** None for Milestone 1.4.
- **Limitations:** The dataset currently focuses on black PLA 3D-printed enclosures. Expanding the dataset to include white, transparent, or resin-printed enclosures will be considered in future dataset iterations (v2).
