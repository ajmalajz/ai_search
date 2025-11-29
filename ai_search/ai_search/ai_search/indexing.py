import frappe
import json
from ai_search.utils import get_embedding, cosine_similarity

INDEX_DOCTYPE = "AI Search Index"


# ==========================================================
# Helpers for inserting / updating / removing index entries
# ==========================================================

def upsert_index(doctype_name: str, docname: str, search_text: str,
                 doctype_filter: str, extra_info: str = ""):
    """Insert or update AI index entry."""
    if not search_text:
        return

    emb = get_embedding(search_text)
    if not emb:
        return

    existing = frappe.db.exists(INDEX_DOCTYPE, {
        "doctype_name": doctype_name,
        "docname": docname,
    })

    payload = {
        "doctype_name": doctype_name,
        "docname": docname,
        "search_text": search_text,
        "embedding": json.dumps(emb),
        "doctype_filter": doctype_filter,
        "score_hint": 0,
        "extra_info": extra_info[:200],
    }

    if existing:
        doc = frappe.get_doc(INDEX_DOCTYPE, existing)
        for k, v in payload.items():
            setattr(doc, k, v)
        doc.save(ignore_permissions=True)
    else:
        payload["doctype"] = INDEX_DOCTYPE
        frappe.get_doc(payload).insert(ignore_permissions=True)


def delete_index(doctype_name: str, docname: str):
    """Delete AI index entry."""
    name = frappe.db.exists(INDEX_DOCTYPE, {
        "doctype_name": doctype_name,
        "docname": docname,
    })
    if name:
        frappe.delete_doc(INDEX_DOCTYPE, name, ignore_permissions=True)


# ==========================================================
# Index Builder — Items
# ==========================================================

def build_index_for_items():
    """Rebuild index for all Items."""
    items = frappe.get_all(
        "Item",
        filters={"disabled": 0},
        fields=[
            "name",
            "item_code",
            "item_name",
            "custom_item_name_arabic",
            "custom_full_description",
            "item_group",
        ],
        limit=0,
    )

    # Load barcodes (child table)
    barcodes_by_item = {}
    rows = frappe.get_all(
        "Item Barcode",
        fields=["parent", "barcode"],
        limit=0,
    )
    for r in rows:
        barcodes_by_item.setdefault(r.parent, []).append(r.barcode)

    for it in items:
        parts = [
            it.item_code or "",
            it.item_name or "",
            it.custom_item_name_arabic or "",
            it.custom_full_description or "",
            it.item_group or "",
        ]

        # add barcodes
        for bc in barcodes_by_item.get(it.name, []):
            parts.append(bc or "")

        search_text = " ".join(parts).replace("\n", " ").strip()
        label = f"{it.item_code or ''} {it.item_name or ''}".strip()

        upsert_index("Item", it.name, search_text, "Item", extra_info=label)

    frappe.db.commit()


# ==========================================================
# Index Builder — Customers
# ==========================================================

def build_index_for_customers():
    customers = frappe.get_all(
        "Customer",
        fields=["name", "customer_name", "customer_type", "customer_group"],
        limit=0,
    )
    for c in customers:
        parts = [
            c.customer_name or "",
            c.customer_type or "",
            c.customer_group or "",
            c.name or "",
        ]
        search_text = " ".join(parts)
        upsert_index("Customer", c.name, search_text, "Customer", extra_info=c.customer_name)
    frappe.db.commit()


# ==========================================================
# Index Builder — Suppliers
# ==========================================================

def build_index_for_suppliers():
    suppliers = frappe.get_all(
        "Supplier",
        fields=["name", "supplier_name", "supplier_type", "supplier_group"],
        limit=0,
    )
    for s in suppliers:
        parts = [
            s.supplier_name or "",
            s.supplier_type or "",
            s.supplier_group or "",
            s.name or "",
        ]
        search_text = " ".join(parts)
        upsert_index("Supplier", s.name, search_text, "Supplier", extra_info=s.supplier_name)
    frappe.db.commit()


# ==========================================================
# Doc Events — Auto Sync
# ==========================================================

def on_item_after_save(doc, method=None):
    parts = [
        doc.item_code or "",
        doc.item_name or "",
        getattr(doc, "custom_item_name_arabic", "") or "",
        getattr(doc, "custom_full_description", "") or "",
        doc.item_group or "",
    ]
    # add child barcodes
    for row in getattr(doc, "barcodes", []) or []:
        parts.append(row.barcode or "")

    search_text = " ".join(parts)
    label = f"{doc.item_code or ''} {doc.item_name or ''}".strip()

    upsert_index("Item", doc.name, search_text, "Item", extra_info=label)


def on_item_trash(doc, method=None):
    delete_index("Item", doc.name)


def on_customer_after_save(doc, method=None):
    parts = [
        doc.customer_name or "",
        doc.customer_type or "",
        doc.customer_group or "",
        doc.name or "",
    ]
    search_text = " ".join(p_
