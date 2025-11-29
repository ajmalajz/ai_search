import frappe
import json
import re
from ai_search.utils import get_embedding, cosine_similarity


# ==============================
# Text Highlighting
# ==============================

def make_highlight(text: str, query: str) -> str:
    """Highlight matched query words using <mark> tag."""
    text = text or ""
    q = (query or "").strip()
    if not q:
        return text

    words = [w for w in re.split(r"\s+", q) if w]
    highlighted = text

    # highlight each query word
    for w in words:
        pattern = re.compile(re.escape(w), re.IGNORECASE)
        highlighted = pattern.sub(lambda m: f"<mark>{m.group(0)}</mark>", highlighted)

    return highlighted


# ==============================
# Generic AI Search
# ==============================

@frappe.whitelist()
def ai_search(query: str, doctype_filter: str = "Item", limit: int = 20):
    """Generic semantic search for any indexed doctype."""
    query = (query or "").strip()
    if not query:
        return []

    # get query embedding
    q_emb = get_embedding(query)
    if not q_emb:
        return []

    rows = frappe.get_all(
        "AI Search Index",
        filters={"doctype_filter": doctype_filter},
        fields=["doctype_name", "docname", "search_text", "extra_info", "embedding"],
    )

    scored = []
    for r in rows:
        try:
            emb = json.loads(r.embedding or "[]")
        except Exception:
            continue

        score = cosine_similarity(q_emb, emb)
        scored.append((score, r))

    # sort: highest score first
    scored.sort(key=lambda x: x[0], reverse=True)

    results = []
    for score, r in scored[: int(limit)]:
        highlight = make_highlight(r.search_text, query)

        results.append({
            "doctype": r.doctype_name,
            "name": r.docname,
            "label": r.extra_info or r.docname,
            "search_text": r.search_text,
            "highlight": highlight,
            "score": score,
        })

    return results


# ==============================
# Item Link Search Override
# ==============================

@frappe.whitelist()
def ai_item_link_query(doctype, txt, searchfield, start, page_len, filters=None):
    matches = ai_search(txt, doctype_filter="Item", limit=page_len)

    out = []
    for m in matches:
        item = frappe.get_value(
            "Item",
            m["name"],
            ["item_code", "item_name"],
            as_dict=True,
        )
        if not item:
            continue

        label = item.item_name or item.item_code
        desc = m["highlight"]

        out.append([item.item_code, label, desc])

    return out


# ==============================
# Customer Link Search Override
# ==============================

@frappe.whitelist()
def ai_customer_link_query(doctype, txt, searchfield, start, page_len, filters=None):
    matches = ai_search(txt, doctype_filter="Customer", limit=page_len)
    return [[m["name"], m["label"]] for m in matches]


# ==============================
# Supplier Link Search Override
# ==============================

@frappe.whitelist()
def ai_supplier_link_query(doctype, txt, searchfield, start, page_len, filters=None):
    matches = ai_search(txt, doctype_filter="Supplier", limit=page_len)
    return [[m["name"], m["label"]] for m in matches]


# ==============================
# Manual Rebuild Endpoints
# ==============================

@frappe.whitelist()
def rebuild_item_index():
    from ai_search.indexing import build_index_for_items
    build_index_for_items()
    return "Item AI index rebuilt."


@frappe.whitelist()
def rebuild_customer_index():
    from ai_search.indexing import build_index_for_customers
    build_index_for_customers()
    return "Customer AI index rebuilt."


@frappe.whitelist()
def rebuild_supplier_index():
    from ai_search.indexing import build_index_for_suppliers
    build_index_for_suppliers()
    return "Supplier AI index rebuilt."
