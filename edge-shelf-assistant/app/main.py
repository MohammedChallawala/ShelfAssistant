from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from tempfile import NamedTemporaryFile
from pathlib import Path
import shutil

from . import vision, speech, db, tts
from .llm import chat
from .config import CONFIDENCE_THRESHOLD

app = FastAPI(title="Edge Shelf Assistant (Sim)")

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Edge Shelf Assistant</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
            .endpoint { background: #f5f5f5; padding: 15px; margin: 10px 0; border-radius: 5px; }
            .method { font-weight: bold; color: #0066cc; }
            .url { font-family: monospace; background: #e8e8e8; padding: 2px 6px; border-radius: 3px; }
            .description { color: #666; margin-top: 5px; }
            .links { margin: 20px 0; }
            .links a { display: inline-block; margin: 5px 10px 5px 0; padding: 10px 15px; 
                       background: #0066cc; color: white; text-decoration: none; border-radius: 5px; }
        </style>
    </head>
    <body>
        <h1>🛒 Edge Shelf Assistant</h1>
        <p>Welcome to your AI-powered shelf assistant! Use the endpoints below to interact with the system.</p>
        
        <div class="links">
            <a href="/docs" target="_blank">📚 Interactive API Docs</a>
            <a href="/redoc" target="_blank">📖 ReDoc API Docs</a>
            <a href="/health">💚 Health Check</a>
        </div>
        
        <h2>Available Endpoints:</h2>
        
        <div class="endpoint">
            <div class="method">GET</div>
            <div class="url">/health</div>
            <div class="description">Check if the service is running properly</div>
        </div>
        
        <div class="endpoint">
            <div class="method">POST</div>
            <div class="url">/vision</div>
            <div class="description">Upload an image file to detect products on shelves</div>
        </div>
        
        <div class="endpoint">
            <div class="method">POST</div>
            <div class="url">/stt</div>
            <div class="description">Upload an audio file for speech-to-text transcription</div>
        </div>
        
        <div class="endpoint">
            <div class="method">POST</div>
            <div class="url">/ask</div>
            <div class="description">Ask questions about products (requires Ollama to be running)</div>
        </div>
        
        <div class="endpoint">
            <div class="method">POST</div>
            <div class="url">/tts</div>
            <div class="description">Convert text to speech and return audio file</div>
        </div>
        
        <h2>Getting Started:</h2>
        <p>1. For the <strong>/ask</strong> endpoint to work, you need Ollama running with the 'phi' model</p>
        <p>2. Use the interactive docs at <a href="/docs">/docs</a> to test the API endpoints</p>
        <p>3. The vision endpoint uses YOLOv8 for product detection</p>
    </body>
    </html>
    """

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/vision")
async def vision_detect(file: UploadFile = File(...)):
    with NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name
    detections = vision.detect(tmp_path, conf=CONFIDENCE_THRESHOLD)
    Path(tmp_path).unlink(missing_ok=True)
    return {"detections": detections}

@app.post("/stt")
async def stt(audio: UploadFile = File(...)):
    with NamedTemporaryFile(delete=False, suffix=Path(audio.filename).suffix) as tmp:
        shutil.copyfileobj(audio.file, tmp)
        tmp_path = tmp.name
    text = speech.transcribe(tmp_path)
    Path(tmp_path).unlink(missing_ok=True)
    return {"text": text}

@app.post("/ask")
async def ask(query: str = Form(...)):
    # simple RAG: search products by keyword, then summarize with LLM
    products = db.get_all()
    matches = db.query_by_keyword(query)
    if not matches:
        context = "Products:\n" + "\n".join([f"- {k}: {v}" for k, v in products.items()])
    else:
        context = "Matched Products:\n" + "\n".join([f"- {k}: {v}" for k, v in matches.items()])
    system = "You are a concise supermarket shelf assistant. Answer using the provided product context only."
    user = f"Context:\n{context}\n\nQuestion: {query}\nKeep it under 80 words."
    answer = chat(system, user)
    return {"answer": answer, "matches": matches}

@app.post("/tts")
async def tts_api(text: str = Form(...)):
    out_path = Path("speech.wav").resolve()
    tts.speak_to_file(text, str(out_path))
    return FileResponse(str(out_path), media_type="audio/wav", filename="speech.wav")
