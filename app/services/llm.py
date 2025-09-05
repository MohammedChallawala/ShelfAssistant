import requests
from typing import Optional, Dict, Any
from .db import db_service
from ..config import OLLAMA_BASE_URL, OLLAMA_MODEL

DEFAULT_SYSTEM_PROMPT = (
    "You are a concise supermarket shelf assistant. Use ONLY the provided product context. "
    "If the answer is not in the context, say you don't know. Keep answers under 120 words."
)

CAPTION_SYSTEM_PROMPT = (
    "You are an image captioning assistant for supermarket shelves. "
    "Produce a brief, plain-text description of the image content."
)

REFINEMENT_SYSTEM_PROMPT = (
    "You are a helpful assistant that refines image analysis outputs. "
    "Take the raw image analysis and provide a clean, natural language explanation "
    "that directly answers the user's query about the image."
)

class LLMService:
    def __init__(self):
        self.base_url = OLLAMA_BASE_URL.rstrip('/')
        self.text_model = "phi3:mini"  # Updated to phi3:mini for text generation
        self.vision_model = "moondream"  # For image analysis
        self.is_connected = False

    def _ping(self) -> bool:
        try:
            resp = requests.get(f"{self.base_url}/api/tags", timeout=3)
            if resp.ok:
                self.is_connected = True
                return True
            self.is_connected = False
            return False
        except Exception:
            self.is_connected = False
            return False

    def get_service_status(self) -> Dict[str, Any]:
        status = {
            "service_name": "Ollama",
            "endpoint": self.base_url,
            "text_model": self.text_model,
            "vision_model": self.vision_model,
            "is_connected": self._ping(),
            "status": "ok" if self.is_connected else "unreachable",
        }
        return status

    def set_text_model(self, model_name: str):
        self.text_model = model_name

    def set_vision_model(self, model_name: str):
        self.vision_model = model_name

    def generate_answer(
        self,
        question: str,
        context: str = "",
        system_prompt: Optional[str] = None,
        temperature: float = 0.2,
        top_p: float = 0.9,
        repeat_penalty: float = 1.1,
        max_tokens: Optional[int] = None,
    ) -> str:
        if not self._ping():
            raise RuntimeError(
                f"Cannot reach Ollama at {self.base_url}. Ensure 'ollama serve' is running and the model is pulled."
            )

        sys_prompt = system_prompt or DEFAULT_SYSTEM_PROMPT
        prompt_parts = []
        if context:
            prompt_parts.append(f"Context:\n{context}\n")
        prompt_parts.append(f"Question: {question}\nAnswer:")
        full_prompt = "\n".join(prompt_parts)

        payload = {
            "model": self.text_model,
            "prompt": f"{sys_prompt}\n\n{full_prompt}",
            "stream": False,
            "options": {
                "temperature": temperature,
                "top_p": top_p,
                "repeat_penalty": repeat_penalty,
            },
        }
        if max_tokens is not None:
            payload["options"]["num_predict"] = max_tokens

        resp = requests.post(f"{self.base_url}/api/generate", json=payload, timeout=60)
        if not resp.ok:
            raise RuntimeError(f"Ollama error {resp.status_code}: {resp.text}")
        data = resp.json()
        return data.get("response", "")

    def analyze_image(self, image_path: str, prompt: str) -> str:
        """Analyze an image using moondream model for vision understanding."""
        if not self._ping():
            raise RuntimeError(
                f"Cannot reach Ollama at {self.base_url}. Ensure 'ollama serve' is running and moondream model is pulled."
            )

        # Convert image to base64 for Ollama API
        import base64
        with open(image_path, 'rb') as f:
            b64 = base64.b64encode(f.read()).decode('utf-8')

        payload = {
            "model": self.vision_model,
            "prompt": prompt,
            "images": [b64],
            "stream": False,
            "options": {"temperature": 0.2}
        }

        resp = requests.post(f"{self.base_url}/api/generate", json=payload, timeout=120)
        if not resp.ok:
            raise RuntimeError(f"Ollama vision error {resp.status_code}: {resp.text}")
        
        data = resp.json()
        return data.get("response", "")

    def image_to_text(self, image_path: str, user_query: str) -> str:
        """Two-stage pipeline: moondream for image analysis, then phi3:mini for refinement."""
        # Stage 1: Raw image analysis with moondream
        moondream_output = self.analyze_image(image_path, user_query)
        
        # Stage 2: Refine with phi3:mini
        refinement_prompt = f"Raw image analysis: {moondream_output}\n\nUser query: {user_query}"
        
        payload = {
            "model": self.text_model,
            "prompt": f"{REFINEMENT_SYSTEM_PROMPT}\n\n{refinement_prompt}",
            "stream": False,
            "options": {"temperature": 0.3}
        }

        resp = requests.post(f"{self.base_url}/api/generate", json=payload, timeout=60)
        if not resp.ok:
            raise RuntimeError(f"Ollama refinement error {resp.status_code}: {resp.text}")
        
        data = resp.json()
        return data.get("response", "")

    def generate_text(self, prompt: str) -> str:
        """Generate text using phi3:mini model."""
        return self.generate_answer(question=prompt, context="", system_prompt=None)

    def voice_query(self, audio_path: str) -> str:
        """Complete voice query pipeline: STT -> LLM response.
        
        Args:
            audio_path: Path to the audio file
            
        Returns:
            LLM response to the transcribed question
        """
        from .stt import stt_service
        
        # Step 1: Transcribe audio to text
        transcript = stt_service.transcribe_audio(audio_path)
        
        # Step 2: Generate response using the transcript
        response = self.generate_text(transcript)
        
        return response

    def caption_image(self, image_path: str, prompt: Optional[str] = None) -> str:
        """Caption an image using moondream model for vision understanding."""
        user_prompt = prompt or "Describe the image succinctly."
        return self.analyze_image(image_path, user_prompt)

    def build_product_context(self, query: Optional[str]) -> Dict[str, Any]:
        if query:
            matches = db_service.search_products(query)
        else:
            matches = db_service.get_all_products()
        if matches:
            lines = [
                f"- #{p['id']} | {p.get('name','')} | {p.get('category','')} | {p.get('price','')} | {p.get('shelf_location','')}"
                for p in matches
            ]
            context = "Products:\n" + "\n".join(lines)
        else:
            context = "Products: (none)"
        return {"context": context, "matches": matches}

# Global LLM service instance
llm_service = LLMService()
