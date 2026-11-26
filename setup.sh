#!/usr/bin/env bash
# One-time setup in a fresh Linux workspace: python deps + Kokoro voice model.
set -e
cd "$(dirname "$0")"
pip install --break-system-packages -q -r requirements.txt
mkdir -p models
[ -f models/kokoro-v1.0.onnx ] || curl -sL -o models/kokoro-v1.0.onnx https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
[ -f models/voices-v1.0.bin ] || curl -sL -o models/voices-v1.0.bin https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
command -v ffmpeg >/dev/null || (apt-get update -q && apt-get install -y -q ffmpeg)
git config user.name >/dev/null || git config user.name "Dr Lumen Bot"
git config user.email >/dev/null || git config user.email "bot@users.noreply.github.com"
echo "setup ok"
