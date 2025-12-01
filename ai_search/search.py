import frappe
from fuzzywuzzy import fuzz

# Custom search override using SQLite or fuzzy matching
def custom_search(doctype, txt, searchfield=None, start=0, page_len=20, filters=None):
    # Fetch items from Item doctype
    results = []
    fields = ['item_code', 'item_name', 'description', 'custom_item_name_arabic', 'custom_search_tags']
    query = f"SELECT name, item_name FROM `tabItem` WHERE disabled=0"
    data = frappe.db.sql(query, as_dict=True)

    for row in data:
        combined = ' '.join([str(row.get(f, '')) for f in fields])
        if fuzz.partial_ratio(txt.lower(), combined.lower()) > 70:
            results.append([row['name'], row['item_name']])

    return results[:page_len]
