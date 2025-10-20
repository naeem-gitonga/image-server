#!/usr/bin/env bash
uv run python - << 'PY'
import torch, sys
print("Python:", sys.executable)
print("Torch:", torch.__version__)
print("Torch CUDA tag:", torch.version.cuda)
print("CUDA available:", torch.cuda.is_available())
if torch.cuda.is_available():
    print("GPU:", torch.cuda.get_device_name(0))
PY
