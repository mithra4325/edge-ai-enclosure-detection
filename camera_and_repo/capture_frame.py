#!/usr/bin/env python3
"""
M1.1: Camera Frame Capture Script
Captures a validation frame from the physical USB webcam connected to Raspberry Pi 5.
"""

import cv2
import sys
import os

def capture_first_frame(device_index=0, output_path="first_frame.jpg"):
    print(f"[INFO] Opening V4L2 camera device at index {device_index} (/dev/video{device_index})...")
    cap = cv2.VideoCapture(device_index)
    
    if not cap.isOpened():
        print(f"[ERROR] Could not access camera on /dev/video{device_index}")
        sys.exit(1)
        
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    # Warm up sensor for automatic exposure/gain adjustment
    print("[INFO] Warming up camera sensor (5 frames)...")
    for _ in range(5):
        cap.read()
        
    ret, frame = cap.read()
    if not ret or frame is None:
        print("[ERROR] Failed to read frame from camera.")
        cap.release()
        sys.exit(1)
        
    h, w, c = frame.shape
    print(f"[SUCCESS] Captured frame: {w}x{h} ({c} channels)")
    
    cv2.imwrite(output_path, frame)
    print(f"[SUCCESS] Frame written to {output_path}")
    cap.release()

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "first_frame.jpg"
    capture_first_frame(0, out)
