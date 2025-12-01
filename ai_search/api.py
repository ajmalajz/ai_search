
import requests
import frappe
from typing import List

MEILI_URL = frappe.conf.get("meili_url")
API_KEY = frappe.conf.get("meili_api_key")
INDEX = "items"

@frappe.whitelist()
def search_items(query: str, limit: int = 20):
    _check_meili_config()
    resp = requests.post(f"{MEILI_URL}/indexes/{INDEX}/search",
                         headers=_headers(), json={"q": query, "limit": limit}, timeout=8)
    return resp.json()

@frappe.whitelist()
def setup_index():
    _check_meili_config()
    settings = {
        "searchableAttributes": ["item_name", "description", "item_code", "name"],
        "displayedAttributes": ["name", "item_code", "item_name", "description"],
        "filterableAttributes": ["item_code"],
        "typoTolerance": {"enabled": True},
        "rankingRules": ["words", "typo", "proximity", "attribute", "exactness"]
    }
    requests.patch(f"{MEILI_URL}/indexes/{INDEX}/settings", headers=_headers(), json=settings, timeout=8)
    return {"ok": True}

@frappe.whitelist()
def bulk_sync_items(batch_size: int = 1000):
    _check_meili_config()
    fields = ["name", "item_code", "item_name", "description"]
    items = frappe.get_all("Item", fields=fields)
    payload: List[dict] = []
    count = 0
    for it in items:
        payload.append(it)
        if len(payload) >= batch_size:
            _post_docs(payload)
            count += len(payload)
            payload = []
    if payload:
        _post_docs(payload)
        count += len(payload)
    return {"indexed": count}

def _post_docs(docs):
    requests.post(f"{MEILI_URL}/indexes/{INDEX}/documents", headers=_headers(), json=docs, timeout=15)

def _headers():
    return {"Authorization": f"Bearer {API_KEY}"} if API_KEY else {}

def _check_meili_config():
    if not MEILI_URL:
        raise frappe.ValidationError("Meilisearch not configured")
