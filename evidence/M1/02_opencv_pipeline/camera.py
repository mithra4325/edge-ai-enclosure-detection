"""
USB Webcam Capture Module for Raspberry Pi 5
Provides low-latency, threaded frame acquisition to prevent buffer lag.
"""

import sys
import time
import threading
from typing import Optional, Tuple
import cv2


class WebcamStream:
    """Threaded VideoCapture reader ensuring real-time frames without buffer queue buildup."""

    def __init__(self, src: int = 0, width: int = 640, height: int = 480, fps: int = 30):
        self.src = src
        self.width = width
        self.height = height
        self.fps = fps

        self.cap = cv2.VideoCapture(self.src)
        if not self.cap.isOpened():
            raise RuntimeError(f"Could not open camera device at index {self.src}")

        # Set hardware properties
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.cap.set(cv2.CAP_PROP_FPS, self.fps)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        # Query actual negotiated settings
        self.actual_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.actual_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.actual_fps = self.cap.get(cv2.CAP_PROP_FPS)

        self.grabbed, self.frame = self.cap.read()
        if not self.grabbed or self.frame is None:
            raise RuntimeError(f"Camera opened, but failed to grab initial frame at index {self.src}")

        self.stopped = False
        self.lock = threading.Lock()
        self.thread = threading.Thread(target=self._update, daemon=True)

    def start(self):
        """Starts the background frame reader thread."""
        self.thread.start()
        return self

    def _update(self):
        """Continuously grab the latest frame in background."""
        while not self.stopped:
            grabbed, frame = self.cap.read()
            if not grabbed:
                continue
            with self.lock:
                self.grabbed = grabbed
                self.frame = frame

    def read(self) -> Tuple[bool, Optional[cv2.Mat]]:
        """Returns the freshest captured frame."""
        with self.lock:
            if not self.grabbed or self.frame is None:
                return False, None
            return True, self.frame.copy()

    def get_info(self) -> dict:
        return {
            "index": self.src,
            "resolution": f"{self.actual_width}x{self.actual_height}",
            "fps": self.actual_fps,
            "status": "online" if self.grabbed else "error"
        }

    def stop(self):
        """Stops the thread and releases the webcam."""
        self.stopped = True
        if self.thread.is_alive():
            self.thread.join(timeout=1.0)
        if self.cap.isOpened():
            self.cap.release()
