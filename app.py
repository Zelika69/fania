import os
from flask import Flask, jsonify, render_template, request
from dotenv import load_dotenv
from services.translator import translate_code

load_dotenv()

app = Flask(__name__)


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

    return jsonify({"success": True, **result})


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=True)