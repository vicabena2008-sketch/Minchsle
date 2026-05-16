"""
app.py
Gradio UI — entry point for local dev and Render deployment.
Run: python app.py
"""

import gradio as gr
from chat import chat
from retrieval import retrieve_context, split_by_stock
from image_fetcher import fetch_product_image, extract_product_name
from conversation import ConversationState


def create_state() -> ConversationState:
    return ConversationState()


def respond(message: str, history: list, state: ConversationState):
    if not message.strip():
        return history, "", state

    reply = chat(message, state)

    # Attach product image if an in-stock result was found
    retrieved = retrieve_context(message, top_k=1)
    in_stock_docs, _ = split_by_stock(retrieved) if retrieved else ([], [])
    if in_stock_docs:
        product_name = extract_product_name(in_stock_docs)
        if product_name:
            image_url = fetch_product_image(product_name)
            if image_url:
                reply += f"\n\n![{product_name}]({image_url})"

    history = history + [
        {"role": "user", "content": message},
        {"role": "assistant", "content": reply},
    ]
    return history, "", state


def clear_chat(state: ConversationState):
    state.reset()
    return [], state


# ── Gradio UI ─────────────────────────────────────────────────────────────────
with gr.Blocks(
    title="Min Chale AI",
) as demo:

    gr.Markdown("""
    # 🤖 Min Chale AI — Shop Assistant 🇬🇭
    **Ask me anything about Tech, Fashion, Food, Home Appliances or Beauty.**
    """)

    chatbot = gr.Chatbot(height=600, label="Min Chale AI", render_markdown=True)
    msg_box = gr.Textbox(
        placeholder="e.g. Recommend a phone under GHS 3000 | Do you have Kente? | Deliver to Kumasi?",
        label="Your message",
        lines=2,
    )

    with gr.Row():
        send_btn  = gr.Button("Send 📨",        variant="primary")
        clear_btn = gr.Button("Clear Chat 🗑️",  variant="secondary")

    session = gr.State(create_state)

    gr.Examples(
        examples=[
            "Recommend a phone under GHS 3000",
            "Do you have Smart TV in stock?",
            "I need a laptop for a student, budget GHS 5000",
            "What snacks do you have for events?",
            "Do you deliver to Kumasi?",
            "Show me rice and gari prices",
            "Recommend something for a birthday gift under GHS 500",
            "Abeg you get Samsung for like 3000?",
            "I need jeans, do you have any?",
        ],
        inputs=msg_box,
    )

    send_btn.click(respond,     inputs=[msg_box, chatbot, session], outputs=[chatbot, msg_box, session])
    msg_box.submit(respond,     inputs=[msg_box, chatbot, session], outputs=[chatbot, msg_box, session])
    clear_btn.click(clear_chat, inputs=[session],                   outputs=[chatbot, session])


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 7860))
    demo.launch(
        server_name="0.0.0.0",
        server_port=port,
        theme=gr.themes.Soft(primary_hue="blue", secondary_hue="orange"),
    )
