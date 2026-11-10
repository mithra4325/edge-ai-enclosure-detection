#!/usr/bin/env python3
"""
Edge AI Enclosure Detection Inference Engine
Deployed on Raspberry Pi 5 with USB Webcam and OpenCV.
Integrates EnclosureDetector, WebcamStream, and SystemMonitor.

Author: Mithra Ravi (mithra4325)
Project: edge-ai-enclosure-detection
Hardware: Raspberry Pi 5 Model B (ARM64)
"""

import argparse
import sys
import time
from pathlib import Path
from collections import deque
import cv2
import numpy as np

# Add src/ to Python path if executed directly
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.camera import WebcamStream
from src.detector import EnclosureDetector
from src.monitor import SystemMonitor


def run_camera_detection(
    model_path: str = "models/best.pt",
    camera_index: int = 0,
    conf_thresh: float = 0.25,
    show_window: bool = True,
    save_evidence_dir: str = "evidence/live_detection",
    benchmark_csv: str = "evidence/benchmark/baseline_results.csv",
    max_frames: int = 0
):
    """
    Runs live real-time enclosure detection on USB webcam frames.
    """
    print("=" * 65)
    print(" EDGE AI ENCLOSURE DETECTION - RASPBERRY PI 5 ")
    print("=" * 65)
    print(f"[*] Model Path:      {model_path}")
    print(f"[*] Camera Device:   Index {camera_index}")
    print(f"[*] Conf Threshold:  {conf_thresh}")
    print(f"[*] Display Window:  {show_window}")
    print(f"[*] Benchmark CSV:   {benchmark_csv}")
    print("=" * 65)

    # Initialize modules
    detector = EnclosureDetector(model_path=model_path, conf_thresh=conf_thresh)
    monitor = SystemMonitor(log_csv_path=benchmark_csv)

    print(f"[*] Opening USB Webcam stream on index {camera_index}...")
    stream = WebcamStream(src=camera_index, width=640, height=480, fps=30)
    stream.start()
    cam_info = stream.get_info()
    print(f"[*] Camera initialized: Resolution={cam_info['resolution']}, Status={cam_info['status']}")

    evidence_path = Path(save_evidence_dir)
    evidence_path.mkdir(parents=True, exist_ok=True)

    frame_count = 0
    fps_history = deque(maxlen=15)

    window_name = "Edge AI Enclosure Detector - Raspberry Pi 5"
    if show_window:
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)
        cv2.resizeWindow(window_name, 640, 480)

    print("[*] Live detection active. Press 'q' to exit, 's' to save snapshot.")

    try:
        while True:
            loop_start = time.perf_counter()

            ret, frame = stream.read()
            if not ret or frame is None:
                time.sleep(0.01)
                continue

            frame_count += 1

            # Run Object Detection with original trained model
            detections, latency_ms = detector.detect(frame)

            # Compute loop timing & rolling FPS
            loop_elapsed = time.perf_counter() - loop_start
            instant_fps = 1.0 / max(loop_elapsed, 1e-4)
            fps_history.append(instant_fps)
            avg_fps = sum(fps_history) / len(fps_history)

            # Retrieve system telemetry (CPU usage, RAM, Temp)
            sys_stats = monitor.get_system_stats()

            # Record baseline benchmark metrics
            monitor.log_benchmark(
                frame_index=frame_count,
                fps=avg_fps,
                inference_latency_ms=latency_ms,
                objects_detected=len(detections)
            )

            # Render HUD overlay and bounding boxes
            annotated = detector.annotate_frame(
                frame=frame,
                detections=detections,
                fps=avg_fps,
                latency_ms=latency_ms,
                system_stats=sys_stats
            )

            # Save key evidence snapshots
            if frame_count in [1, 5, 10, 20, 30] or (frame_count % 100 == 0):
                snapshot_file = evidence_path / f"live_frame_{frame_count:04d}.jpg"
                cv2.imwrite(str(snapshot_file), annotated)

            # Display live OpenCV GUI
            if show_window:
                cv2.imshow(window_name, annotated)
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q') or key == ord('Q') or key == 27:  # 'q' or ESC
                    print("\n[*] 'q' key pressed. Stopping live detection...")
                    break
                elif key == ord('s') or key == ord('S'):
                    manual_snap = evidence_path / f"manual_snapshot_{int(time.time())}.jpg"
                    cv2.imwrite(str(manual_snap), annotated)
                    print(f"[*] Snapshot saved: {manual_snap}")

            if max_frames > 0 and frame_count >= max_frames:
                print(f"[*] Reached target test frame limit: {max_frames} frames.")
                break

    except KeyboardInterrupt:
        print("\n[*] Interrupted by user (Ctrl+C).")
    finally:
        stream.stop()
        if show_window:
            cv2.destroyAllWindows()
        monitor.close()
        print(f"[*] Session closed cleanly. Total processed frames: {frame_count}")
        print(f"[*] Benchmark metrics saved to: {benchmark_csv}")


def run_file_inference(
    model_path: str,
    source: str,
    conf_thresh: float = 0.25,
    save_dir: str = "evidence/model_test"
):
    """
    Runs detection on a single image file or directory of images.
    """
    detector = EnclosureDetector(model_path=model_path, conf_thresh=conf_thresh)
    source_path = Path(source)
    if not source_path.exists():
        raise FileNotFoundError(f"Source path not found: {source_path}")

    image_files = []
    if source_path.is_file():
        image_files.append(source_path)
    else:
        valid_exts = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
        image_files = sorted([p for p in source_path.iterdir() if p.suffix.lower() in valid_exts])

    save_path = Path(save_dir)
    save_path.mkdir(parents=True, exist_ok=True)

    print(f"[*] Running inference on {len(image_files)} sample image(s)...")
    total_detections = 0

    for idx, img_path in enumerate(image_files, start=1):
        img = cv2.imread(str(img_path))
        if img is None:
            print(f"[!] Warning: Could not read image: {img_path}")
            continue

        detections, latency_ms = detector.detect(img)
        total_detections += len(detections)

        print(f"[{idx}/{len(image_files)}] {img_path.name}: {len(detections)} enclosure(s) found (Latency: {latency_ms:.1f}ms)")
        for i, det in enumerate(detections, start=1):
            bbox = det["bbox"]
            conf = det["confidence"]
            name = det["class_name"]
            print(f"    - Detection {i}: Class '{name}' | Confidence: {conf * 100:.2f}% | Box: {bbox}")

        dummy_stats = {
            "cpu_percent": 0.0,
            "cpu_temp_c": SystemMonitor.get_cpu_temp(),
            "ram_used_mb": SystemMonitor.get_ram_usage()["used_mb"]
        }
        annotated = detector.annotate_frame(
            frame=img,
            detections=detections,
            fps=1000.0 / max(latency_ms, 1e-5),
            latency_ms=latency_ms,
            system_stats=dummy_stats
        )

        out_file = save_path / f"pred_{img_path.name}"
        cv2.imwrite(str(out_file), annotated)

    print(f"[*] Offline test complete. Total detections: {total_detections}")
    print(f"[*] Annotated results saved to: {save_path.resolve()}")


def main():
    parser = argparse.ArgumentParser(description="Edge AI Enclosure Detection System (Raspberry Pi 5)")
    parser.add_argument("--model", type=str, default="models/best.pt", help="Path to model weights (.pt or .onnx)")
    parser.add_argument("--source", type=str, default="0", help="Camera index (0) or path to image/folder")
    parser.add_argument("--conf", type=float, default=0.25, help="Confidence threshold (default: 0.25)")
    parser.add_argument("--save-dir", type=str, default="evidence/live_detection", help="Directory for output evidence")
    parser.add_argument("--benchmark-csv", type=str, default="evidence/benchmark/baseline_results.csv", help="CSV benchmark file")
    parser.add_argument("--show", action="store_true", default=False, help="Display live OpenCV GUI window")
    parser.add_argument("--max-frames", type=int, default=0, help="Optional max frames limit (0 = continuous)")
    args = parser.parse_args()

    # Determine if source is camera device or static images
    is_cam = args.source.isdigit() or args.source.startswith("/dev/video")
    if is_cam:
        cam_idx = int(args.source) if args.source.isdigit() else 0
        run_camera_detection(
            model_path=args.model,
            camera_index=cam_idx,
            conf_thresh=args.conf,
            show_window=args.show,
            save_evidence_dir=args.save_dir,
            benchmark_csv=args.benchmark_csv,
            max_frames=args.max_frames
        )
    else:
        run_file_inference(
            model_path=args.model,
            source=args.source,
            conf_thresh=args.conf,
            save_dir=args.save_dir
        )


if __name__ == "__main__":
    main()
