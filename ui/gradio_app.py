import gradio as gr
import requests
import os

API_BASE = os.getenv("API_BASE", "http://localhost:8000")

def do_detect(img):
    if img is None:
        return "Upload an image."
    import PIL.Image
    import io
    buf = io.BytesIO()
    PIL.Image.fromarray(img).save(buf, format="PNG")
    buf.seek(0)
    files = {"file": ("upload.png", buf, "image/png")}
    r = requests.post(f"{API_BASE}/vision", files=files, timeout=120)
    r.raise_for_status()
    return r.json()

def do_stt(audio):
    if audio is None:
        return "Record or upload audio."
    files = {"audio": (audio.name, open(audio.name, "rb"), audio.mime_type)}
    r = requests.post(f"{API_BASE}/stt", files=files, timeout=300)
    r.raise_for_status()
    return r.json().get("text", "")

def do_ask(q):
    r = requests.post(f"{API_BASE}/ask", data={"query": q}, timeout=120)
    r.raise_for_status()
    return r.json().get("answer", "")

def do_voice_query(audio):
    """Process voice query: transcribe and get LLM response."""
    if audio is None:
        return "Record or upload audio.", "No audio provided."
    
    try:
        files = {"audio": (audio.name, open(audio.name, "rb"), "audio/wav")}
        r = requests.post(f"{API_BASE}/llm/voice", files=files, timeout=120)
        r.raise_for_status()
        data = r.json()
        return data["data"]["transcript"], data["data"]["response"]
    except Exception as e:
        return f"Error: {str(e)}", f"Error: {str(e)}"

with gr.Blocks() as demo:
    gr.Markdown("# Edge Shelf Assistant (Sim)")
    with gr.Tab("Vision"):
        img = gr.Image(label="Upload product/shelf image")
        out = gr.JSON()
        btn = gr.Button("Detect")
        btn.click(do_detect, inputs=img, outputs=out)
    with gr.Tab("Speech → Text"):
        aud = gr.Audio(sources=["microphone", "upload"], type="filepath")
        stt_out = gr.Textbox(label="Transcription")
        stt_btn = gr.Button("Transcribe")
        stt_btn.click(do_stt, inputs=aud, outputs=stt_out)
    with gr.Tab("Ask Shelf"):
        q = gr.Textbox(label="Your question")
        a = gr.Textbox(label="Answer")
        ask_btn = gr.Button("Ask")
        ask_btn.click(do_ask, inputs=q, outputs=a)
    
    with gr.Tab("Voice"):
        gr.Markdown("### 🎤 Voice Query")
        gr.Markdown("Record your question or upload an audio file. The system will transcribe it and provide an AI response.")
        
        voice_audio = gr.Audio(
            sources=["microphone", "upload"], 
            type="filepath",
            label="Record or upload audio"
        )
        
        with gr.Row():
            transcript_box = gr.Textbox(
                label="Transcription", 
                placeholder="Your spoken question will appear here...",
                lines=2
            )
            response_box = gr.Textbox(
                label="AI Response", 
                placeholder="AI response will appear here...",
                lines=4
            )
        
        voice_btn = gr.Button("🎤 Process Voice Query", variant="primary")
        voice_btn.click(
            do_voice_query, 
            inputs=voice_audio, 
            outputs=[transcript_box, response_box]
        )

if __name__ == "__main__":
    demo.launch(server_port=7860)
