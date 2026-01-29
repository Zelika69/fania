import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

DEFAULT_MODEL = "gemini-3-flash-preview"


class GeminiClient:
    def __init__(self, api_key: str | None = None, model_id: str | None = None) -> None:
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model_id = model_id or DEFAULT_MODEL

        if not self.api_key:
            raise RuntimeError("GEMINI_API_KEY is not set")

        self.client = genai.Client(api_key=self.api_key)

    def generate(self, prompt: str) -> str:
        response = self.client.models.generate_content(
            model=self.model_id,
            contents=prompt,
        )

        text = getattr(response, "text", None)
        if not text:
            raise RuntimeError("Respuesta inesperada de Gemini. Intenta nuevamente.")
        return text.strip()