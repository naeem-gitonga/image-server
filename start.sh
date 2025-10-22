#!/bin/sh
set -e

APP_IMPORT="app.main:app"
HOST="0.0.0.0"
PORT="80"
WORKERS="1"

# paths to ignore (space separated string instead of array)
IGNORE_PATHS=".git .venv .cache $HOME/.cache $HOME/hf_cache /tmp"

# Activate venv (POSIX compatible)
if [ -z "${VIRTUAL_ENV:-}" ]; then
  if [ -d ".venv" ]; then
    . .venv/bin/activate
  else
    echo "❌ .venv not found. Run: python3 -m venv .venv" >&2
    exit 1
  fi
fi

# Install missing dependencies
pip install --quiet --upgrade watchfiles uvicorn[standard] --break-system-packages
pip install --quiet --upgrade huggingface_hub diffusers transformers peft accelerate safetensors pillow --break-system-packages

# Hugging Face cache tweaks
export HF_HOME="${HF_HOME:-$HOME/hf_cache}"
export HF_HUB_ENABLE_HF_TRANSFER=1
export TRANSFORMERS_NO_ADVISORY_WARNINGS=1
export PYTHONUNBUFFERED=1

# Build ignore flags for watchfiles
IGNORE_FLAGS=""
for p in $IGNORE_PATHS; do
  if [ -d "$p" ] || echo "$p" | grep -q "cache"; then
    IGNORE_FLAGS="$IGNORE_FLAGS --ignore-paths $p"
  fi
done

echo "▶️  Starting DEV server (sh compatible)..."
exec watchfiles --target-type=command \
  $IGNORE_FLAGS \
  "uvicorn $APP_IMPORT --host $HOST --port $PORT --workers $WORKERS" .
