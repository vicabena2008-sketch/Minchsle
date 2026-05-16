"""
retrieval.py
Builds the FAISS index from knowledge_base and exposes retrieve_context().
"""

# pyrefly: ignore [missing-import]
import faiss
# pyrefly: ignore [missing-import]
import numpy as np
import os
import json
from knowledge_base import business_data

# Optional imports
try:
    # prefer sentence-transformers if available for local builds
    from sentence_transformers import SentenceTransformer
except Exception:
    SentenceTransformer = None

try:
    import openai
except Exception:
    openai = None

RELEVANCE_THRESHOLD = 0.30

# Look for a prebuilt index to avoid loading an embedding model at runtime
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
INDEX_PATH = os.path.join(DATA_DIR, "index.faiss")
DOCS_PATH = os.path.join(DATA_DIR, "documents.json")
METADATA_PATH = os.path.join(DATA_DIR, "doc_metadata.json")

# Globals filled below
index = None
documents: list[str] = []
doc_metadata: list[dict] = []
embedding_model = None

# Try to load prebuilt index + documents
if os.path.exists(INDEX_PATH) and os.path.exists(DOCS_PATH) and os.path.exists(METADATA_PATH):
    print("Loading prebuilt FAISS index and documents from data/ ...")
    index = faiss.read_index(INDEX_PATH)
    with open(DOCS_PATH, 'r', encoding='utf-8') as f:
        documents = json.load(f)
    with open(METADATA_PATH, 'r', encoding='utf-8') as f:
        doc_metadata = json.load(f)
    print(f"✅ Loaded FAISS index ({index.ntotal} vectors) and {len(documents)} documents.")
else:
    # Build index at import time (fallback). This will load a model and may be memory heavy.
    print("No prebuilt index found — building FAISS index (this may use significant memory)...")
    # Build documents + metadata from knowledge_base
    documents = []
    doc_metadata = []
    for item in business_data:
        stock_tag = "IN STOCK" if item["in_stock"] else "OUT OF STOCK"
        count_tag = f" (qty: {item['stock_count']})" if item["stock_count"] is not None else ""

        doc = (
            f"[CATEGORY: {item['category'].upper()}]\n"
            f"BRAND / TYPE: {item.get('brand', 'General')}\n"
            f"STOCK STATUS: {stock_tag}{count_tag}\n"
            f"DETAILS: {item['content']}"
        ).strip()

        documents.append(doc)
        doc_metadata.append({
            "in_stock": item["in_stock"],
            "category": item["category"],
            "brand": item["brand"],
        })

    # Try to load a sentence-transformer model if available
    if SentenceTransformer is not None:
        embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
        print("Encoding documents...")
        embeddings = np.array(embedding_model.encode(documents, convert_to_numpy=True), dtype=np.float32)
        faiss.normalize_L2(embeddings)
        index = faiss.IndexFlatIP(embeddings.shape[1])
        index.add(embeddings)
        print(f"✅ FAISS index ready — {index.ntotal} vectors.")
    else:
        raise RuntimeError("No prebuilt index found and sentence-transformers is not available.\n" \
                           "Run build_index.py locally and upload the data/ folder, or install sentence-transformers.")




# ── Public API ────────────────────────────────────────────────────────────────
def _embed_query_with_openai(text: str) -> np.ndarray:
    """Return an embedding vector using OpenAI if configured."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key or openai is None:
        return None
    openai.api_key = api_key
    resp = openai.Embedding.create(model="text-embedding-3-small", input=text)
    vec = np.array(resp['data'][0]['embedding'], dtype=np.float32)
    # normalize
    vec = vec.reshape(1, -1)
    faiss.normalize_L2(vec)
    return vec


def retrieve_context(user_query: str, top_k: int = 5) -> list[tuple]:
    """Returns [(score, doc_text, metadata), ...] sorted by score DESC."""
    if not user_query.strip():
        return []

    # 1) Try to embed using local embedding_model (if present)
    if embedding_model is not None:
        q_emb = np.array(embedding_model.encode([user_query], convert_to_numpy=True), dtype=np.float32)
        faiss.normalize_L2(q_emb)
        scores, indices = index.search(q_emb.astype(np.float32), top_k)
    else:
        # 2) Try OpenAI embeddings if configured
        q_emb = _embed_query_with_openai(user_query)
        if q_emb is not None:
            scores, indices = index.search(q_emb.astype(np.float32), top_k)
        else:
            # 3) Fallback: simple token overlap scoring (cheap, not semantic)
            q_tokens = set(user_query.lower().split())
            scored = []
            for i, doc in enumerate(documents):
                score = len(q_tokens.intersection(set(doc.lower().split())))
                scored.append((float(score), i))
            scored.sort(key=lambda x: x[0], reverse=True)
            # emulate FAISS output shape
            scores = [[s for s, _ in scored[:top_k]]]
            indices = [[idx for _, idx in scored[:top_k]]]

    results = []
    for score, idx in zip(scores[0], indices[0]):
        if idx != -1 and score >= RELEVANCE_THRESHOLD:
            results.append((float(score), documents[idx], doc_metadata[idx]))

    results.sort(key=lambda x: x[0], reverse=True)
    return results


def split_by_stock(retrieved: list) -> tuple[list, list]:
    """Returns (in_stock_docs, out_of_stock_brands)."""
    in_stock   = [doc for _, doc, meta in retrieved if meta["in_stock"]]
    oos_brands = [meta["brand"] for _, _, meta in retrieved if not meta["in_stock"]]
    return in_stock, oos_brands
