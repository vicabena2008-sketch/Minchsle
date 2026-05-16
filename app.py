"""
app.py
Gradio UI — entry point for local dev and Render deployment.
Run: python app.py
"""

from chat import chat
from retrieval import retrieve_context, split_by_stock
from image_fetcher import fetch_product_image, extract_product_name
from conversation import ConversationState

from flask import Flask, render_template, request, jsonify
import os
import uuid

app = Flask(__name__, static_folder="static", template_folder="templates")

# In-memory session store: session_id -> ConversationState
sessions: dict[str, ConversationState] = {}


def create_state() -> ConversationState:
    return ConversationState()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/new_session", methods=["POST"])
def new_session():
    sid = str(uuid.uuid4())
    sessions[sid] = create_state()
    return jsonify({"session_id": sid})


@app.route("/api/respond", methods=["POST"])
def api_respond():
    data = request.get_json() or {}
    message = data.get("message", "")
    sid = data.get("session_id")

    if not sid or sid not in sessions:
        sid = str(uuid.uuid4())
        sessions[sid] = create_state()

    state = sessions[sid]

    if not message.strip():
        return jsonify({"reply": "", "session_id": sid, "image_url": None})

    reply = chat(message, state)

    # Optionally attach product image URL if available
    retrieved = retrieve_context(message, top_k=1)
    in_stock_docs, _ = split_by_stock(retrieved) if retrieved else ([], [])
    image_url = None
    if in_stock_docs:
        product_name = extract_product_name(in_stock_docs)
        if product_name:
            image_url = fetch_product_image(product_name)

    return jsonify({"reply": reply, "session_id": sid, "image_url": image_url})


@app.route("/api/clear", methods=["POST"])
def api_clear():
    data = request.get_json() or {}
    sid = data.get("session_id")
    if sid and sid in sessions:
        sessions[sid].reset()
        return jsonify({"ok": True})
    return jsonify({"ok": False}), 400


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    app.run(host="0.0.0.0", port=port)
