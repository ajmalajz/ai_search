
app_name = "ai_search"
app_title = "AI Search"
app_publisher = "Your Company"
app_description = "Meilisearch integration for ERPNext link search"
app_version = "0.1.0"

# Load our JS on common transaction doctypes
doctype_js = {
    "Sales Invoice": "public/js/ai_item_search.js",
    "Sales Order": "public/js/ai_item_search.js",
    "Purchase Order": "public/js/ai_item_search.js",
    "Delivery Note": "public/js/ai_item_search.js",
    "Purchase Receipt": "public/js/ai_item_search.js",
    "Purchase Invoice": "public/js/ai_item_search.js",
    "Stock Entry": "public/js/ai_item_search.js",
    "Material Request": "public/js/ai_item_search.js",
}

# Sync items on insert/update

# For modern Frappe/ERPNext, 'after_insert' is called post-insert; 'on_update' on modify

doc_events = {
    "Item": {
        "after_insert": "ai_search.utils.sync_item",
        "on_update": "ai_search.utils.sync_item",
    }
}

# Optional: scheduler for periodic health or reindex
scheduler_events = {
    "daily": [
        # "ai_search.utils.daily_health_check"
    ]
}
