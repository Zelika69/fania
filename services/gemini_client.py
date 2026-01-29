import os
import requests

GEMINI_API_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-1.5-flash:generateContent"
)


class GeminiClient:
    def __init__(self, api_key: str | None = None, timeout: int = 30) -> None:
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.timeout = timeout

        if not self.api_key:
            raise RuntimeError(
                "No se encontró GEMINI_API_KEY. Configura la variable de entorno."
            )

    def generate(self, prompt: str) -> str:
        url = f"{GEMINI_API_URL}?key={self.api_key}"
        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": prompt}],
                }
            ],
            "generationConfig": {
                "temperature": 0.2,
                "maxOutputTokens": 2048,
                "topP": 0.9,
            },
        }

        response = requests.post(url, json=payload, timeout=self.timeout)
        if response.status_code != 200:
            raise RuntimeError(
                "Error al comunicarse con Gemini. Intenta nuevamente más tarde."
            )

        data = response.json()
        try:
            return data["candidates"][0]["content"]["parts"][0]["text"].strip()
        except (KeyError, IndexError, TypeError) as exc:
            raise RuntimeError(
                "Respuesta inesperada de Gemini. Intenta nuevamente."
            ) from exc