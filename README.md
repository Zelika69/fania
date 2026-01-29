# C# Code Translator

Aplicación web en Flask que traduce código C# a otros lenguajes usando Google Gemini. Incluye opciones para optimizar el resultado y explicar línea por línea.

## Requisitos

- Python 3.10+
- Clave de Google AI Studio (Gemini)

## Configuración de la clave

1. Crea una API key en [Google AI Studio](https://aistudio.google.com/app/apikey).
2. Copia el archivo `.env.example` a `.env` y coloca tu clave:

```bash
cp .env.example .env
```

```env
GEMINI_API_KEY=tu_clave_aqui
```

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Ejecución

```bash
python app.py
```

Luego abre `http://localhost:5000`.

## Endpoints

- `GET /`: interfaz web.
- `POST /translate`: recibe JSON con `{ code, target_lang, optimize, explain }`.

## Notas

- Si el código no parece C#, la app responde con: `Parece que no es C#. Por favor pega C#`.
- Límite de 6000 caracteres por solicitud.