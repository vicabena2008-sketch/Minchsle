"""
conversation.py
ConversationState class and follow-up instruction builder.
"""

import re
from urllib.parse import quote

WHATSAPP_NUMBER = "233557618362"

TOPIC_FOLLOWUPS = {
    "tech":    "Ask if the customer wants warranty details, delivery timeline, or payment options.",
    "home":    "Ask if the customer wants warranty details, delivery timeline, or payment options.",
    "fashion": "Ask if they need a different size, colour, or matching accessories.",
    "food":    "Ask if they need bulk/wholesale pricing or event packaging.",
    "beauty":  "Ask if they want a product bundle or recommendation for their skin type.",
}
DEFAULT_FOLLOWUP = (
    "Ask if there is anything else from our categories "
    "(Tech, Fashion, Food, Home, Beauty) you can help with."
)

NO_ANSWER_FALLBACK = (
    "I'm sorry, I don't have information about that in our current catalogue. "
    "Please reach out to us on WhatsApp at +233 5576 183 62 and our team will assist you right away. "
    "Is there anything else from our current stock I can help you with?"
)


# ── WhatsApp handoff ──────────────────────────────────────────────────────────
def build_whatsapp_link(last_user_message: str, product_context: str = "") -> str:
    intro = "Hello! I was chatting with the Min Chale AI assistant and need help with:"
    body  = f"{intro}\n\n\"{last_user_message}\""
    if product_context:
        body += f"\n\nContext: {product_context}"
    return f"https://wa.me/{WHATSAPP_NUMBER}?text={quote(body)}"


# ── Conversation state ────────────────────────────────────────────────────────
class ConversationState:
    def __init__(self):
        self.reset()

    def reset(self):
        self.history:           list[tuple[str, str]] = []
        self.last_resolved:     bool  = True
        self.last_topic:        str | None = None
        self.unanswered_count:  int   = 0
        self.budget_mentioned:  str | None = None

    def record_turn(self, user_msg: str, ai_reply: str, resolved: bool, topic: str | None = None):
        self.history.append((user_msg, ai_reply))
        self.last_resolved = resolved
        if topic:
            self.last_topic = topic
        self.unanswered_count = 0 if resolved else self.unanswered_count + 1

        m = re.search(
            r'(?:GHS?|cedis?)\s*(\d[\d,]+)|(\d[\d,]+)\s*(?:GHS?|cedis)',
            user_msg, re.IGNORECASE
        )
        if m:
            self.budget_mentioned = m.group(0).strip()

    def history_str(self, last_n: int = 6) -> str:
        return "\n".join(
            f"Customer: {q}\nMin Chale AI: {a}"
            for q, a in self.history[-last_n:]
        )


# ── Follow-up instruction builder ────────────────────────────────────────────
def build_followup_instruction(
    state: ConversationState,
    has_context: bool,
    out_of_stock_brands: list[str],
    top_topic: str | None,
) -> str:
    lines = []

    if not has_context:
        if state.unanswered_count == 0:
            lines.append(
                "You could not find a match. Ask ONE focused clarifying question "
                "(budget, category, or purpose) before referring to WhatsApp."
            )
        elif state.unanswered_count == 1:
            lines.append(
                "Still no match. Try a different angle — ask if the customer can "
                "describe what they need differently, or suggest the closest category you carry."
            )
        else:
            wa_link = build_whatsapp_link(
                state.history[-1][0] if state.history else "a product inquiry"
            )
            lines.append(
                f"You have been unable to help for {state.unanswered_count} turns. "
                f"Sincerely apologise and provide this WhatsApp link for human support: {wa_link} "
                "Then ask if anything else from current stock can be helped with."
            )
    else:
        if out_of_stock_brands:
            oos = ", ".join(out_of_stock_brands)
            lines.append(
                f"'{oos}' is currently unavailable. Acknowledge it briefly once, "
                "then recommend the nearest in-stock alternative from the context."
            )
        lines.append(TOPIC_FOLLOWUPS.get(top_topic or "", DEFAULT_FOLLOWUP))
        if state.budget_mentioned:
            lines.append(
                f"The customer mentioned a budget of {state.budget_mentioned}. "
                "If not yet addressed, suggest 1–2 in-stock items within that budget."
            )

    return "\n".join(lines)
