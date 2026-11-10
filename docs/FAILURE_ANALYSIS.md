# Failure Analysis: The White-Surface False-Positive Vulnerability

**Document Status:** Formal Engineering Investigation  
**Author / Lead Investigator:** Mithra Ravi (`mithra4325`)  
**Project:** Edge AI 3D-Printed Enclosure Detection  
**Model Investigated:** Original YOLO Nano (`yolo26n`, `models/best.pt`)  
**Milestone:** M1 Evaluation & M2 Improvement Strategy  

---

## 1. Problem Statement

In academic computer vision, high validation metrics (such as **100% mAP@0.5**) frequently mask operational vulnerabilities when the model encounters real-world environments. During live webcam testing of our trained enclosure detector on the Raspberry Pi 5, an important failure mode was discovered:

> **The model frequently detects non-enclosure white surfaces—including white sheets of paper, light-colored desk edges, pale walls, and laptop lids—as custom enclosures, producing confidence scores between $22\%$ and $48\%$.**

This failure analysis provides a formal investigation of this behavior, presents photographic evidence, proposes scientific hypotheses, and establishes a concrete mitigation plan for Milestone 2.

---

## 2. Empirical Observations & Evidence

| Scenario | Expected Output | Observed Output | Severity |
| :--- | :--- | :--- | :---: |
| **White Enclosure on Workbench** | 1 detection (`enclosure`), conf $>70\%$ | Confirmed: Detected at **74% – 95%** | Nominal |
| **Empty Workbench (Dark Wood)** | 0 detections | Confirmed: 0 bounding boxes | Nominal |
| **White Sheet of Paper in Frame** | 0 detections | **False Positive:** 1-2 bounding boxes on paper corners (conf $25\% – 42\%$) | **Critical** |
| **Light Table Edge / Wall Reflection**| 0 detections | **False Positive:** Spurious boxes on bright boundary transitions | **Moderate** |
| **Live Demo Screenshot 1 (`IMG_9700`)**| 1 true enclosure detected | 1 true enclosure + **5 false-positive proposals** on surrounding light surfaces | **High** |
| **Live Demo Screenshot 2 (`IMG_9701`)**| 1 true enclosure detected | 1 true enclosure + **4 false-positive proposals** on pale boundaries | **High** |

---

## 3. Scientific Hypotheses for the Failure

### Hypothesis A: Background Luminance Bias (The "Dark Workbench" Effect)
- **Dataset Reality:** In Dataset v1, all 40 photographs featured the white PLA enclosure placed exclusively on a dark brown wooden workbench.
- **Learned Feature Representation:** Neural networks minimize loss by finding the most readily separable features. Instead of learning complex high-frequency geometrical features (e.g., circular PIR sensor dome cutout, mounting screw holes, rectangular bevels), the early convolutional filters learned that:
  $$\text{Object Likelihood} \propto \frac{\text{Luminance}(\text{Target})}{\text{Luminance}(\text{Background})}$$
  Because white-on-dark contrast was 100% correlated with positive labels in the training set, the network treats any bright white boundary as a candidate enclosure.

### Hypothesis B: Complete Absence of Hard-Negative Samples
- **Dataset Reality:** Dataset v1 contained 40 positive images and **0 negative background images**.
- **Learned Loss Penalty:** In object detection loss functions (such as YOLO's CIoU + DFL + BCE loss), gradients for the background class ($C_{\text{bg}}$) are only updated when proposed anchors overlap with true background regions within positive images. Because the network was never shown white objects explicitly labeled as "NOT enclosure" (i.e. images with empty label files), the network was never penalized for assigning high confidence to white rectangular shapes.

### Hypothesis C: Limited Geometric Invariance
- **Dataset Reality:** 40 images is sufficient for an initial proof of concept on a static test set, but insufficient for a 2.5-million-parameter network to generalize complex 3D perspective transformations across varied environments without synthetic augmentations.

---

## 4. Operational Impact on Edge AI Systems

In a real-world edge deployment (such as an automated assembly line verification camera or facility security scanner):
1. **High False-Alarm Rate:** Stray documents, workers wearing white lab coats, or light reflections would trigger false positive events.
2. **Degraded Object Counting:** The automated count HUD would fluctuate erratically between 1 and 6 objects depending on background clutter.
3. **Loss of Autonomous Trust:** Downstream actuators or alerting systems cannot rely on detection signals with low background specificity.

---

## 5. Milestone 2 (M2) Comprehensive Mitigation Strategy

The failure cannot be solved simply by tuning the confidence threshold: raising the threshold to $0.50$ suppresses some false positives, but also causes true enclosures at oblique angles (which score $35\% – 45\%$) to be missed (false negatives).

A principled data-centric and architectural strategy will be executed in Milestone 2:

### Strategy 1: Multi-Background Data Collection (Dataset v2)
Collect 60+ new photographic captures across diverse physical backgrounds:
- Light oak / white laminate desks.
- Metallic workbench surfaces and aluminium extrusions.
- Concrete and carpeted laboratory floors.
- High-glare direct window lighting and shadowed conditions.

### Strategy 2: Systematic Hard-Negative Injection
Collect and incorporate 25+ pure **hard-negative images** with **zero bounding boxes**:
- Plain white A4 paper sheets and notebooks.
- White 3D printer scraps and filament spools.
- White power bricks, phone chargers, and rectangular electronics.
- Ambient laboratory rooms with light walls and furniture.

*By including hard negatives with empty label files, YOLO's classification loss explicitly penalizes white-surface activations.*

### Strategy 3: Multi-Scale Domain Augmentations
Introduce domain-specific augmentations during Roboflow v2 export:
- Photometric distortion (brightness jitter $\pm 25\%$, contrast variation $\pm 20\%$).
- Mosaic augmentation and Cutout / Random Erasing to force the network to identify local geometric features rather than relying on global white blobs.

### Strategy 4: Rigorous Comparative Evaluation
Train an improved model (`best_v2.pt`) and evaluate both the M1 baseline model (`best.pt`) and the M2 model on an **identical held-out benchmark test set**:
- Compare mAP@0.5 and mAP@0.5:0.95.
- Compare precision and recall.
- Measure the reduction in false-positive activations on hard-negative test scenes.

---

## 6. Preservation of M1 Baseline Integrity

In strict adherence to academic standards:
- **No weights have been retrained.**
- **No dataset files have been altered or replaced.**
- The original model (`models/best.pt`) and Dataset v1 (`data/`) remain untouched as the authentic baseline for all Milestone 2 comparisons.
