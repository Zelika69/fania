import os
from flask import Flask, jsonify, render_template, request
from dotenv import load_dotenv
from services.history_store import (
    get_translation,
    init_db,
    list_translations,
    save_translation,
)
from services.translator import translate_code

load_dotenv()

app = Flask(__name__)

try:
    init_db()
except Exception:
    pass


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/translate", methods=["POST"])
def translate():
    data = request.get_json(silent=True) or {}
    code = (data.get("code") or "").strip()
    target_lang = (data.get("target_lang") or "").strip()
    optimize = bool(data.get("optimize"))
    explain = bool(data.get("explain"))

    try:
        result = translate_code(
            code=code,
            target_lang=target_lang,
            optimize=optimize,
            explain=explain,
        )
    except ValueError as exc:
        return jsonify({"success": False, "message": str(exc)}), 400
    except RuntimeError as exc:
        return jsonify({"success": False, "message": str(exc)}), 502

    try:
        entry_id = save_translation(
            input_code=code,
            output_code=result["code"],
            explanation=result.get("explanation", ""),
            target_lang=target_lang,
            optimize=optimize,
            explain=explain,
        )
    except Exception:
        return (
            jsonify({"success": False, "message": "No se pudo guardar el historial."}),
            500,
        )

    return jsonify({"success": True, "entry_id": entry_id, **result})


@app.route("/history", methods=["GET"])
def history():
    try:
        entries = list_translations()
    except Exception:
        return jsonify({"success": False, "message": "No se pudo cargar el historial."}), 500
    return jsonify({"success": True, "entries": entries})


@app.route("/history/<int:entry_id>", methods=["GET"])
def history_detail(entry_id: int):
    entry = get_translation(entry_id)
    if not entry:
        return jsonify({"success": False, "message": "Historial no encontrado."}), 404
    return jsonify({"success": True, "entry": entry})


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=True)