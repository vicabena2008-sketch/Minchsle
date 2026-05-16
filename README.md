# Min Chale AI — Shop Assistant

RAG-powered retail chatbot for Min Chale (Accra, Ghana).
Built with Gradio + FAISS + Groq (Llama 3.3 70B).

---

## Project Structure

```
minchale-ai/
├── app.py              # Entry point — Gradio UI
├── chat.py             # Core chat logic
├── retrieval.py        # FAISS index + retrieve_context()
├── knowledge_base.py   # All product/shop data (edit here to update products)
├── llm.py              # Groq LLM setup + system prompt
├── conversation.py     # ConversationState + follow-up builder
├── image_fetcher.py    # DuckDuckGo image fetcher (swap for Cloudinary later)
├── requirements.txt
├── .env.example
└── .gitignore
```

---

## Local Setup (VS Code)

```bash
# 1. Clone / open the folder in VS Code

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set your API key
cp .env.example .env
# Open .env and paste your GROQ_API_KEY

# 5. Run
python app.py
# Open http://localhost:7860
```

---

## Deploy on Render

1. Push this folder to a GitHub repo.
2. Go to [render.com](https://render.com) → **New Web Service** → connect your repo.
3. Set these in **Environment Variables** on Render:
   - `GROQ_API_KEY` = your Groq key
4. Set **Build Command**:
   ```
   pip install -r requirements.txt
   ```
5. Set **Start Command**:
   ```
   python app.py
   ```
6. Click **Deploy** — Render gives you a public URL.

---

## Updating Products

Open `knowledge_base.py` and edit `business_data`.
Each entry follows this shape:

```python
{
    "category": "tech",          # tech | fashion | food | home | beauty | ...
    "brand":    "Samsung",
    "in_stock": True,
    "stock_count": 18,           # None for non-physical items
    "content":  "Description with prices...",
}
```

No other file needs to change when you add/edit products.

---

## Switching to Cloudinary Images (when ready)

In `image_fetcher.py`, replace `fetch_product_image()` with:

```python
PRODUCT_IMAGES = {
    "Samsung":    "https://res.cloudinary.com/YOUR_CLOUD/image/upload/samsung.jpg",
    "Apple":      "https://res.cloudinary.com/YOUR_CLOUD/image/upload/apple.jpg",
    # ...
}

def fetch_product_image(product_name: str) -> str | None:
    for key, url in PRODUCT_IMAGES.items():
        if key.lower() in product_name.lower():
            return url
    return None
```
