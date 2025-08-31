# Edge Shelf Assistant (Laptop Sim + RPi5-ready)

This repository is a **laptop-first simulation** of an edge supermarket shelf assistant,
with a path to deploy on Raspberry Pi 5. It combines **vision (YOLO/MobileNet)**, **speech (Whisper/Vosk)**,
**LLM (Ollama/llama.cpp)**, **SQLite product DB**, and a simple **Gradio UI**.

## Quick Start (Laptop)
1) Install Ollama and pull a tiny model:
```bash
ollama pull phi
ollama serve  # in one terminal
```

2) Create a Python venv and install requirements:
```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

3) (Optional) Download a Whisper model (tiny/base) the first time `faster-whisper` runs.

4) Run the API server:
```bash
uvicorn app.main:app --reload --port 8000
```

5) Launch the UI:
```bash
python ui/gradio_app.py
```

## Docker (Laptop, x86_64)
```bash
docker build -f docker/Dockerfile -t shelf-assistant:latest .
docker run --rm -it -p 8000:8000 --name shelf shelf-assistant:latest
```

## Simulate RPi5 Constraints with Docker
Emulate memory/CPU constraints similar to Pi 5 (8 GB RAM, 4 cores):
```bash
docker run --rm -it -p 8000:8000 --cpus=3.5 --memory=6g shelf-assistant:latest
```

## ARM64 / RPi5 Userland Simulation (on x86 host)
Install qemu-user-static and enable multiarch. Then:
```bash
docker buildx create --use
docker buildx build --platform linux/arm64 -f docker/Dockerfile.arm64 -t shelf-assistant:arm64 --load .
docker run --rm -it -p 8000:8000 --cpus=3.5 --memory=6g shelf-assistant:arm64
```
> This simulates ARM64 userland with CPU/RAM caps (not true Pi GPU/SoC).

## Deploying to actual RPi5 (later)
- Use `docker/Dockerfile.arm64` on the Pi.
- Reduce model sizes: `phi` (Q4), YOLOv8n, Whisper-tiny.
- Consider `llama.cpp` if Ollama performance is insufficient.
