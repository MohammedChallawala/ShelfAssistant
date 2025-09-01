import requests
from typing import Optional, Dict, Any
from .db import db_service
from ..config import OLLAMA_BASE_URL, OLLAMA_MODEL

DEFAULT_SYSTEM_PROMPT = (
    "You are a concise supermarket shelf assistant. Use ONLY the provided product context. "
    "If the answer is not in the context, say you don't know. Keep answers under 120 words."
)

class LLMService:
    def __init__(self):
        self.base_url = OLLAMA_BASE_URL.rstrip('/')
        self.model_name = OLLAMA_MODEL
        self.is_connected = False

    def _ping(self) -> bool:
        try:
            # List installed models to verify service is up
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
            "model_name": self.model_name,
            "is_connected": self._ping(),
            "status": "ok" if self.is_connected else "unreachable",
        }
        return status

    def set_model(self, model_name: str):
        self.model_name = model_name

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
            "model": self.model_name,
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

        resp = requests.post(
            f"{self.base_url}/api/generate",
            json=payload,
            timeout=60,
        )
        if not resp.ok:
            raise RuntimeError(f"Ollama error {resp.status_code}: {resp.text}")
        data = resp.json()
        return data.get("response", "")

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
