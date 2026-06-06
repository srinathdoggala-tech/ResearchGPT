#!/usr/bin/env bash
# Run backend tests inside a Docker container (Linux/macOS)
set -euo pipefail

docker run --rm -v "$(pwd)/backend":/app -w /app python:3.11-slim bash -lc \
  "apt-get update >/dev/null && apt-get install -y gcc >/dev/null && pip install -U pip >/dev/null && pip install -r requirements.txt >/dev/null && pytest -q"
