import frappe
import requests
import math
import json

# ==========
# CONFIG
# ==========

# You can change "text-embedding-3-large" to any multilingual model you want
EMBEDDING_MODEL = "text-embedding-3-large"

# --------
# Helpers
# --------

def get_api_key():
    """Read API key from site_config.json."""
    return frappe.conf.get("ai_search_api_key")


def get_embedding(text: str):
    """Get embedding using OpenAI API (or Groq-compatible)."""
    api_key = get_api_key()
    if not api_key:
        frappe.throw("AI Search API key (ai_search_api_key) not set in site_config.json")

    text = (text or "").strip()
    if not text:
        return []

    try:
        response = requests.post(
            "https://api.openai.com/v1/embeddings",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
            },
            json={
                "model": EMBEDDING_MODEL,
                "input": text,
            },
            timeout=15,
        )
        data = response.json()

        if "error" in data:
            frappe.throw(f"OpenAI Error: {data['error']['message']}")

        raw = data["data"][0]["embedding"]

        # compress vector for speed & size
        compressed = [round(x, 3) for x in raw]

        return compressed

    except Exception as e:
        frappe.log_error(f"AI Search embedding error: {e}")
        return []


def cosine_similarity(a, b):
    """Compute cosine similarity between two vectors."""
    if not a or not b or len(a) != len(b):
        return 0

    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))

    if not norm_a or not norm_b:
        return 0

    return dot / (norm_a * norm_b)
