# Edge Shelf Assistant (Laptop Sim + RPi5-ready)

This repository is a **laptop-first simulation** of an edge supermarket shelf assistant,
with a path to deploy on Raspberry Pi 5. It combines **vision (YOLO/MobileNet)**, **speech (Whisper/Vosk)**,
**LLM (Ollama/llama.cpp)**, **SQLite product DB**, and a simple **Gradio UI**.

## 🚀 New Modular API Structure

The project now includes a **modular FastAPI backend** with the following structure:

```
app/
 ├── __init__.py
 ├── main.py          # Entry point for FastAPI app
 ├── routes/
 │    ├── __init__.py
 │    ├── products.py # CRUD APIs for product shelf data
 │    ├── vision.py   # Placeholder for YOLOv8 shelf recognition
 │    └── llm.py      # Placeholder for local LLM Q&A
 ├── models/
 │    ├── __init__.py
 │    ├── product.py  # Pydantic models for product data
 │    └── response.py # Common response schemas
 └── services/
      ├── __init__.py
      ├── db.py       # SQLite database handler
      ├── vision.py   # Connect YOLOv8 detection (stub for now)
      └── llm.py      # Stub function for local LLM inference
```

### 🛒 Products API (Fully Implemented)

**CRUD Operations:**
- `POST /products` - Create new product
- `GET /products` - List all products (with pagination & search)
- `GET /products/{id}` - Get specific product
- `PUT /products/{id}` - Update product
- `DELETE /products/{id}` - Delete product

**Features:**
- SQLite database with automatic schema creation
- Input validation using Pydantic models
- Pagination and search capabilities
- Comprehensive error handling
- Full test coverage

### 🔮 Future Endpoints (Placeholders)

- **Vision API** (`/vision/*`) - YOLOv8 shelf recognition
- **LLM API** (`/llm/*`) - Local LLM Q&A with RAG support

## Quick Start (Laptop)

### 1. Install Dependencies
```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Start the API Server
```bash
# Option 1: Direct command
uvicorn app.main:app --reload --port 8000

# Option 2: Windows batch file
start_api.bat

# Option 3: Python script
python run.py
```

### 3. Access the API
- **API Base URL**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

### 4. Run Tests
```bash
# Option 1: Direct pytest
pytest tests/ -v

# Option 2: Test runner script
python run_tests.py
```

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
