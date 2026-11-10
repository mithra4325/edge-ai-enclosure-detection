#!/usr/bin/env python3
"""
M1.4: Dataset Annotation Rendering Script
Reads ground-truth YOLO labels for all Train, Valid, and Test splits,
and generates visually annotated images with bounding boxes, corner anchors,
and class badges matching the Roboflow dataset specifications.
"""

import os
import glob
import cv2
import numpy as np

def render_dataset_annotations(base_dir=".", output_dir="dataset_v1/annotated_images", max_dim=1600):
    splits = ["train", "valid", "test"]
    color_bgr = (147, 20, 255) # Deep pink / Roboflow magenta (#ff1493)
    
    total_images = 0
    total_boxes = 0
    
    for split in splits:
        split_out = os.path.join(output_dir, split)
        os.makedirs(split_out, exist_ok=True)
        img_files = sorted(glob.glob(os.path.join(base_dir, "data", split, "images", "*.jpg")))
        print(f"[INFO] Processing {split} split ({len(img_files)} images)...")
        
        for img_path in img_files:
            base_name = os.path.basename(img_path)
            stem = os.path.splitext(base_name)[0]
            label_path = os.path.join(base_dir, "data", split, "labels", stem + ".txt")
            
            img = cv2.imread(img_path)
            if img is None:
                continue
            h, w = img.shape[:2]
            
            boxes = []
            if os.path.exists(label_path):
                with open(label_path, "r") as f:
                    for line in f:
                        parts = line.strip().split()
                        if len(parts) >= 5:
                            cls_id = int(parts[0])
                            xc = float(parts[1]) * w
                            yc = float(parts[2]) * h
                            bw = float(parts[3]) * w
                            bh = float(parts[4]) * h
                            x1 = int(xc - bw / 2.0)
                            y1 = int(yc - bh / 2.0)
                            x2 = int(xc + bw / 2.0)
                            y2 = int(yc + bh / 2.0)
                            boxes.append((x1, y1, x2, y2))
                            total_boxes += 1
            
            # Scale if larger than max_dim
            scale = min(1.0, float(max_dim) / max(w, h))
            if scale < 1.0:
                new_w = int(w * scale)
                new_h = int(h * scale)
                img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)
                boxes = [(int(x1*scale), int(y1*scale), int(x2*scale), int(y2*scale)) for x1, y1, x2, y2 in boxes]
                h, w = new_h, new_w
                
            for i, (x1, y1, x2, y2) in enumerate(boxes):
                # Draw outer bounding box
                cv2.rectangle(img, (x1, y1), (x2, y2), color_bgr, 3, cv2.LINE_AA)
                
                # Corner accents for visual tightness verification
                clen = min(25, (x2-x1)//4, (y2-y1)//4)
                t = 5
                cv2.line(img, (x1, y1), (x1 + clen, y1), (255, 255, 255), t, cv2.LINE_AA)
                cv2.line(img, (x1, y1), (x1, y1 + clen), (255, 255, 255), t, cv2.LINE_AA)
                cv2.line(img, (x2, y1), (x2 - clen, y1), (255, 255, 255), t, cv2.LINE_AA)
                cv2.line(img, (x2, y1), (x2, y1 + clen), (255, 255, 255), t, cv2.LINE_AA)
                cv2.line(img, (x1, y2), (x1 + clen, y2), (255, 255, 255), t, cv2.LINE_AA)
                cv2.line(img, (x1, y2), (x1, y2 - clen), (255, 255, 255), t, cv2.LINE_AA)
                cv2.line(img, (x2, y2), (x2 - clen, y2), (255, 255, 255), t, cv2.LINE_AA)
                cv2.line(img, (x2, y2), (x2, y2 - clen), (255, 255, 255), t, cv2.LINE_AA)
                
                # Label badge
                label = f"enclosure [GT #{i+1}]"
                font = cv2.FONT_HERSHEY_SIMPLEX
                font_scale = 0.7
                thickness = 2
                (tw, th), baseline = cv2.getTextSize(label, font, font_scale, thickness)
                
                tag_y1 = max(0, y1 - th - 10)
                tag_y2 = y1
                tag_x1 = x1
                tag_x2 = x1 + tw + 14
                
                cv2.rectangle(img, (tag_x1, tag_y1), (tag_x2, tag_y2), color_bgr, -1)
                cv2.putText(img, label, (tag_x1 + 7, tag_y2 - 5), font, font_scale, (255, 255, 255), thickness, cv2.LINE_AA)
                
            # Telemetry header banner
            header_text = f"Roboflow Dataset V1 | Split: {split.upper()} | File: {base_name[:25]}... | Objects: {len(boxes)}"
            cv2.rectangle(img, (0, 0), (w, 35), (20, 20, 20), -1)
            cv2.putText(img, header_text, (15, 24), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 255), 2, cv2.LINE_AA)
            
            out_file = os.path.join(split_out, base_name)
            cv2.imwrite(out_file, img, [cv2.IMWRITE_JPEG_QUALITY, 88])
            total_images += 1
            
    print(f"[SUCCESS] Generated {total_images} annotated images with {total_boxes} ground-truth boxes in {output_dir}")

if __name__ == "__main__":
    render_dataset_annotations()
