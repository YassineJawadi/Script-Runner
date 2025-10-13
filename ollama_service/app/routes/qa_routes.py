from flask import Blueprint, request, jsonify, current_app
import requests
import time
from ..services.ollama_client import generate_response

qa_blueprint = Blueprint("qa", __name__)

@qa_blueprint.route("/ask", methods=["POST"])
def ask_question():
    body = request.get_json() or {}
    prompt = body.get("prompt") or body.get("question")
    model = body.get("model") or current_app.config.get("OLLAMA_MODEL")
    max_tokens = body.get("max_tokens") or current_app.config.get("DEFAULT_MAX_TOKENS")

    if not prompt or not isinstance(prompt, str) or not prompt.strip():
        return jsonify({"error": "prompt (string) is required"}), 400

    try:
        start_time = time.time()  # Start timer
        output = generate_response(prompt, model=model, max_tokens=max_tokens)
        elapsed = time.time() - start_time  # End timer
    except requests.RequestException as e:
        return jsonify({"error": "model call failed", "details": str(e)}), 502
    except Exception as e:
        return jsonify({"error": "model call failed", "details": str(e)}), 502

    return jsonify({
        "model": model,
        "raw": output,
        "time_taken_seconds": round(elapsed, 2)  # Add elapsed time
    }), 200
