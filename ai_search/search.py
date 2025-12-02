import frappe
from fuzzywuzzy import fuzz

def custom_search(doctype, txt, searchfield=None, start=0, page_len=20, filters=None):
    # Simple fuzzy match over Item fields
    fields = ['item_code','item_name','description','custom_item_name_arabic','custom_search_tags']
    res=[]
    data=frappe.db.sql("SELECT name, item_name, description FROM `tabItem` WHERE disabled=0", as_dict=True)
    q=txt or ''
    for row in data:
        combined=' '.join([str(row.get(f,'')) for f in fields])
        try:
            score=fuzz.partial_ratio(q.lower(), combined.lower())
        except Exception:
            score=0
        if score>=70:
            res.append([row['name'], row.get('item_name') or row['name']])
    return res[:page_len]
