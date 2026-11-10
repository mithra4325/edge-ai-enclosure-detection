"""
Raspberry Pi 5 System & Performance Telemetry Monitor
Tracks CPU Usage, RAM Usage, CPU Temperature, Latency, and FPS.
Logs baseline benchmark metrics to CSV.
"""

import os
import time
import csv
from pathlib import Path
from typing import Optional, Dict, Any
import psutil


class SystemMonitor:
    """Monitors Raspberry Pi 5 hardware statistics and model performance."""

    def __init__(self, log_csv_path: Optional[str] = None):
        self.log_csv_path = Path(log_csv_path) if log_csv_path else None
        self.csv_file = None
        self.csv_writer = None
        self._init_csv()

        # Telemetry cache
        self.last_temp = self.get_cpu_temp()
        self.last_cpu_percent = 0.0
        self.last_telemetry_time = time.time()

    def _init_csv(self):
        if self.log_csv_path:
            self.log_csv_path.parent.mkdir(parents=True, exist_ok=True)
            file_exists = self.log_csv_path.exists()
            self.csv_file = open(self.log_csv_path, mode="a", newline="", encoding="utf-8")
            self.csv_writer = csv.writer(self.csv_file)
            if not file_exists or os.path.getsize(self.log_csv_path) == 0:
                self.csv_writer.writerow([
                    "timestamp",
                    "frame_index",
                    "fps",
                    "inference_latency_ms",
                    "cpu_usage_pct",
                    "ram_usage_mb",
                    "cpu_temp_c",
                    "objects_detected"
                ])
                self.csv_file.flush()

    @staticmethod
    def get_cpu_temp() -> float:
        """Reads Raspberry Pi onboard thermal sensor (°C)."""
        try:
            with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
                return round(float(f.read().strip()) / 1000.0, 1)
        except Exception:
            return 0.0

    @staticmethod
    def get_ram_usage() -> Dict[str, float]:
        """Returns RAM used in MB and percentage."""
        vm = psutil.virtual_memory()
        return {
            "used_mb": round(vm.used / (1024 * 1024), 1),
            "total_mb": round(vm.total / (1024 * 1024), 1),
            "percent": round(vm.percent, 1)
        }

    def get_system_stats(self) -> Dict[str, Any]:
        """Polls hardware telemetry without blocking the inference loop."""
        now = time.time()
        # Refresh CPU usage and temp at most every 0.5s to keep overhead minimal
        if now - self.last_telemetry_time > 0.5:
            self.last_cpu_percent = round(psutil.cpu_percent(interval=None), 1)
            self.last_temp = self.get_cpu_temp()
            self.last_telemetry_time = now

        ram = self.get_ram_usage()
        return {
            "cpu_percent": self.last_cpu_percent,
            "cpu_temp_c": self.last_temp,
            "ram_used_mb": ram["used_mb"],
            "ram_percent": ram["percent"],
            "inference_backend": "CPU (Raspberry Pi 5 ARM Cortex-A76)"
        }

    def log_benchmark(self, frame_index: int, fps: float, inference_latency_ms: float, objects_detected: int):
        """Logs a single inference benchmark record to the CSV file."""
        if not self.csv_writer:
            return

        stats = self.get_system_stats()
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

        self.csv_writer.writerow([
            timestamp,
            frame_index,
            round(fps, 2),
            round(inference_latency_ms, 2),
            stats["cpu_percent"],
            stats["ram_used_mb"],
            stats["cpu_temp_c"],
            objects_detected
        ])
        self.csv_file.flush()

    def close(self):
        if self.csv_file and not self.csv_file.closed:
            self.csv_file.close()
