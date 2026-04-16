"""
calndr.ai — Flask backend

Run locally:
 
    Windows (PowerShell):
        $env:GEMINI_API_KEY="your-key-here"
        python app.py
"""

import os
import sys
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

#  Config
API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    sys.exit(
        "\n[calndr.ai] GEMINI_API_KEY is not set.\n"
        "  macOS/Linux:  export GEMINI_API_KEY='your-key'\n"
        "  Windows PS :  $env:GEMINI_API_KEY='your-key'\n"
    )

MODEL_NAME = "gemini-2.0-flash"   # swap if you prefer a different model
MAX_TURNS = 20                     # cap history to the last N exchanges
MAX_MESSAGE_LEN = 2000             # reject absurdly long inputs

SYSTEM_PROMPT = """You are calndr.ai, an expert time management coach for college students. Your role is to:
- Help students organize their schedules and prioritize tasks
- Suggest study techniques (Pomodoro method, time blocking, etc.)
- Create realistic timelines for assignments and exams
- Help reduce procrastination and stress
- Offer advice on balancing academics, extracurriculars, and self-care

Be friendly, supportive, and practical. Keep responses concise and actionable."""

# ——— Setup ————————————————————————————————————————————————
logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(levelname)s  %(message)s")
log = logging.getLogger("calndr")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(
    model_name=MODEL_NAME,
    system_instruction=SYSTEM_PROMPT,   # cleaner than injecting as a user turn
)

app = Flask(__name__)
CORS(app)  # allow the HTML file to call us from file:// or a different port

# in-memory session (one user, fine for local dev)
conversation_history = []


# Helper
def trim_history(history, max_turns=MAX_TURNS):
    """Keep only the most recent N user+model pairs."""
    if len(history) <= max_turns * 2:
        return history
    return history[-(max_turns * 2):]


def build_contents(history, user_msg):
    """Build the contents list Gemini expects."""
    return history + [{"role": "user", "parts": [{"text": user_msg}]}]


# Routes
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "model": MODEL_NAME})


@app.route("/reset", methods=["POST"])
def reset():
    global conversation_history
    conversation_history = []
    return jsonify({"ok": True})


@app.route("/chat", methods=["POST"])
def chat():
    global conversation_history

    # —— validate input ——
    data = request.get_json(silent=True) or {}
    user_msg = (data.get("message") or "").strip()

    if not user_msg:
        return jsonify({"error": "empty message"}), 400
    if len(user_msg) > MAX_MESSAGE_LEN:
        return jsonify({"error": f"message too long (max {MAX_MESSAGE_LEN} chars)"}), 400

    # call the model 
    try:
        contents = build_contents(conversation_history, user_msg)
        response = model.generate_content(contents)
        reply = (response.text or "").strip()
        if not reply:
            reply = "hmm, I didn't get a response that time. mind rephrasing?"
    except Exception as e:
        # log the full error server-side, but never leak it to the client
        log.exception("gemini call failed")
        return jsonify({
            "reply": "I'm having trouble reaching my brain right now. try again in a moment?"
        }), 200

    # update history (only on success) 
    conversation_history.append({"role": "user",  "parts": [{"text": user_msg}]})
    conversation_history.append({"role": "model", "parts": [{"text": reply}]})
    conversation_history = trim_history(conversation_history)

    return jsonify({"reply": reply})


#  Entry point 
if __name__ == "__main__":
    log.info(f"calndr.ai backend starting on http://127.0.0.1:5000  (model: {MODEL_NAME})")
    app.run(host="127.0.0.1", port=5000, debug=False)





