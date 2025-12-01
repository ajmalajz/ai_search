
import requests
import frappe
from typing import List

MEILI_URL = frappe.conf.get("meili_url")
API_KEY = frappe.conf.get("meili_api_key")
INDEX = "items"

@frappe.whitelist()
def search_items(query: str, limit: int = 20):
    _check_meili_config()
    try:
        resp = requests.post(
            f"{MEILI_URL}/indexes/{INDEX}/search",
            headers=_headers(),
            json={"q": query, "limit": limit},
            timeout=8,
        )
        resp.raise_for_status()
        return resp.json()
    except Exception:
        frappe.log_error(frappe.get_traceback(), title="ai_search.search_items error")
        return {"hits": []}

@frappe.whitelist()
def setup_index():
    _check_meili_config()
    settings = {
        "searchableAttributes": ["item_name", "description", "item_code", "name"],
        "displayedAttributes": ["name", "item_code", "item_name", "description"],
        "filterableAttributes": ["item_code"],
        "typoTolerance": {"enabled": True},
        "rankingRules": ["words", "typo", "proximity", "attribute", "exactness"],
    }
    resp = requests.patch(
        f"{MEILI_URL}/indexes/{INDEX}/settings",
        headers=_headers(),
        json=settings,
        timeout=8,
    )
    resp.raise_for_status()
    return {"ok": True}

@frappe.whitelist()
def bulk_sync_items(batch_size: int = 1000):
    _check_meili_config()
    fields = ["name", "item_code", "item_name", "description"]
    items = frappe.get_all("Item", fields=fields)
    payload: List[dict] = []
    count = 0
    for it in items:
        payload.append({
            "name": it["name"],
            "item_code": it.get("item_code"),
            "item_name": it.get("item_name"),
            "description": it.get("description"),
        })
        if len(payload) >= batch_size:
            _post_docs(payload)
            count += len(payload)
            payload = []
    if payload:
        _post_docs(payload)
        count += len(payload)
    return {"indexed": count}

@frappe.whitelist()
def link_search_items(doctype: str, txt: str, searchfield: str, start: int, page_len: int, filters=None):
    tokens = [t.strip() for t in (txt or '').split() if t.strip()]
    limit = page_len or 20
    offset = start or 0

    if _is_meili_configured():
        try:
            resp = requests.post(
                f"{MEILI_URL}/indexes/{INDEX}/search",
                headers=_headers(),
                json={"q": txt, "limit": limit, "offset": offset},
                timeout=6,
            )
            resp.raise_for_status()
            hits = resp.json().get("hits", [])
            out = []
            for h in hits:
                code = h.get("item_code") or h.get("name")
                name = h.get("item_name") or h.get("description") or h.get("name")
                out.append([code, name])
            return out
        except Exception:
            frappe.log_error(frappe.get_traceback(), title="ai_search.link_search_items Meili error")

    # Fallback: token AND search on DB (supports Arabic/English since LIKE is UTF-8)
    conds = []
    params = []
    for t in tokens:
        conds.append("(item_name LIKE %s OR description LIKE %s OR item_code LIKE %s)")
        like = f"%{t}%"
        params.extend([like, like, like])
    where = " AND ".join(conds) if conds else "1=1"
    q = f"""
        SELECT item_code, item_name
        FROM `tabItem`
        WHERE disabled=0 AND {where}
        ORDER BY modified DESC
        LIMIT %s OFFSET %s
    """
    params.extend([limit, offset])
    rows = frappe.db.sql(q, params)
    return [[r[0] or '', r[1] or ''] for r in rows]

# ---------------- helpers -----------------

def _headers():
    if API_KEY:
        return {"Authorization": f"Bearer {API_KEY}"}
    return {}

def _is_meili_configured():
    return bool(MEILI_URL)

def _check_meili_config():
    if not MEILI_URL:
        raise frappe.ValidationError("Meilisearch is not configured. Set 'meili_url' and 'meili_api_key' in site_config.json")

def _post_docs(docs: List[dict]):
    resp = requests.post(
        f"{MEILI_URL}/indexes/{INDEX}/documents",
        headers=_headers(),
        json=docs,
        timeout=15,
    )
    resp.raise_for_status()
