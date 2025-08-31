#!/usr/bin/env bash
# Simulate Pi 5 constraints via Docker resource caps (Linux/macOS with Docker Desktop)
# Usage: ./scripts/simulate_pi_constraints.sh
set -euo pipefail

IMAGE=${1:-shelf-assistant:latest}
docker run --rm -it -p 8000:8000 --cpus=3.5 --memory=6g "$IMAGE"
