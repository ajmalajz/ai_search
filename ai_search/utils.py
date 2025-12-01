
import requests
import frappe

MEILI_URL = frappe.conf.get("meili_url")
API_KEY = frappe.conf.get("meili_api_key")
INDEX = "items"
HEADERS = {"Authorization": f"Bearer {API_KEY}"} if API_KEY else {}

def sync_item(doc, method=None):
    if not MEILI_URL:
        return
    data = {
        "name": doc.name,
        "item_code": doc.item_code,
        "item_name": doc.item_name,
        "description": doc.description
    }
    requests.post(f"{MEILI_URL}/indexes/{INDEX}/documents", headers=HEADERS, json=[data], timeout=8)
