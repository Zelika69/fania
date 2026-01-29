import re
from services.gemini_client import GeminiClient

SUPPORTED_LANGUAGES = {"Python", "JavaScript", "TypeScript", "Java", "Go"}
MAX_CHARS = 6000


def _looks_like_csharp(code: str) -> bool:
    patterns = [
        r"using\s+System",
        r"namespace\s+\w+",
        r"Console\.WriteLine",
        r"\bpublic\s+class\b",
        r"\bstatic\s+void\s+Main\b",
        r"\bstring\s+\w+\s*=",
    ]
    return any(re.search(pattern, code) for pattern in patterns)


def _build_prompt(code: str, target_lang: str, optimize: bool, explain: bool) -> str:
    optimization = (
        "Optimiza el código traducido (nombres claros, manejo de null, errores, "
        "complejidad y estilo idiomático del lenguaje destino)."
        if optimize
        else "Conserva el estilo original sin optimizaciones adicionales."
    )

    explain_rule = (
        "Responde con dos secciones exactas en este formato:\n"
        "---CODE---\n"
        "(solo el código traducido, sin fences)\n"
        "---EXPLANATION---\n"
        "(explicación línea por línea en español)."
        if explain
        else "Responde solo con el código traducido, sin explicaciones ni markdown."
    )

    return (
        "Eres un traductor estricto de C# a otros lenguajes. "
        "Sigue las instrucciones de salida al pie de la letra. "
        "No inventes APIs inexistentes. Mantén la lógica original.\n"
        f"Lenguaje destino: {target_lang}.\n"
        "La entrada siempre debería ser C#. Si no parece C#, responde exactamente: "
        "Parece que no es C#. Por favor pega C#\n"
        f"{optimization}\n"
        f"{explain_rule}\n"
        "Código C# de entrada:\n"
        "```\n"
        f"{code}\n"
        "```\n"
    )


def _parse_response(text: str, explain: bool) -> dict:
    if not explain:
        return {"code": text.strip(), "explanation": ""}

    if "---CODE---" not in text or "---EXPLANATION---" not in text:
        raise RuntimeError("Respuesta inválida del modelo. Intenta de nuevo.")

    code_part = text.split("---CODE---", 1)[1].split("---EXPLANATION---", 1)[0]
    explanation_part = text.split("---EXPLANATION---", 1)[1]

    return {
        "code": code_part.strip(),
        "explanation": explanation_part.strip(),
    }


def translate_code(code: str, target_lang: str, optimize: bool, explain: bool) -> dict:
    if not code:
        raise ValueError("El código está vacío. Pega tu código C#.")

    if len(code) > MAX_CHARS:
        raise ValueError("El código supera el límite de 6000 caracteres.")

    if target_lang not in SUPPORTED_LANGUAGES:
        raise ValueError("Selecciona un lenguaje destino válido.")

    if not _looks_like_csharp(code):
        raise ValueError("Parece que no es C#. Por favor pega C#")

    prompt = _build_prompt(code, target_lang, optimize, explain)
    client = GeminiClient()
    response_text = client.generate(prompt)

    if response_text.strip() == "Parece que no es C#. Por favor pega C#":
        raise ValueError("Parece que no es C#. Por favor pega C#")

    return _parse_response(response_text, explain)