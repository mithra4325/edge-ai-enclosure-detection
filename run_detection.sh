#!/usr/bin/env bash
# ==============================================================================
# Edge AI 3D-Printed Enclosure Detection - Raspberry Pi 5 Launcher
# Launches the live object detection pipeline using original YOLO Nano weights.
# ==============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Ensure DISPLAY and Qt backend are set for GUI window on local desktop
export DISPLAY="${DISPLAY:-:0}"
export WAYLAND_DISPLAY="${WAYLAND_DISPLAY:-wayland-0}"
export QT_QPA_PLATFORM="xcb"

# Virtual environment path
VENV_PATH="$SCRIPT_DIR/venv"

if [ ! -d "$VENV_PATH" ]; then
    echo "[!] Virtual environment not found at: $VENV_PATH"
    echo "[*] Creating virtual environment with system site packages..."
    python3 -m venv --system-site-packages "$VENV_PATH"
    "$VENV_PATH/bin/pip" install --extra-index-url https://download.pytorch.org/whl/cpu torch torchvision ultralytics onnxruntime
fi

source "$VENV_PATH/bin/activate"

echo "=================================================================="
echo " Starting Edge AI Enclosure Detection on Raspberry Pi 5"
echo " Model:    models/best.pt"
echo " Camera:   USB Webcam (/dev/video0)"
echo " GUI:      Active on $DISPLAY (Press 'q' in window to exit)"
echo " Evidence: evidence/live_detection & evidence/benchmark"
echo "=================================================================="

# Pass any user-supplied flags, or default to live camera detection with GUI display
if [ $# -eq 0 ]; then
    python src/inference.py --model models/best.pt --source 0 --show
else
    python src/inference.py "$@"
fi
