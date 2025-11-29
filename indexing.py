import frappe
from ai_search.utils import clean_text

def get_item_text(item):
    doc = frappe.get_doc("Item", item)

    text = " ".join([
        doc.item_code or "",
        doc.item_name or "",
        getattr(doc, "custom_item_name_arabic", "") or "",
        getattr(doc, "custom_full_description", "") or "",
    ])

    return clean_text(text)

def on_item_after_save(doc, event):
    content = get_item_text(doc.name)

    if frappe.db.exists("AI Search Index", doc.name):
        frappe.db.set_value("AI Search Index", doc.name, "content", content)
    else:
        new = frappe.get_doc({
            "doctype": "AI Search Index",
            "name": doc.name,
            "reference_doctype": "Item",
            "reference_name": doc.name,
            "content": content,
        })
        new.insert(ignore_permissions=True)

def on_item_trash(doc, event):
    if frappe.db.exists("AI Search Index", doc.name):
        frappe.delete_doc("AI Search Index", doc.name, ignore_permissions=True)
