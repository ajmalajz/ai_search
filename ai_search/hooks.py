
app_name = "ai_search"
app_title = "AI Search"
app_publisher = "Your Company"
app_description = "Meilisearch integration for ERPNext with Arabic support"
app_version = "1.0.0"

doctype_js = {
    "Sales Invoice": "public/js/ai_item_search.js",
    "Sales Order": "public/js/ai_item_search.js",
    "Purchase Order": "public/js/ai_item_search.js",
    "Delivery Note": "public/js/ai_item_search.js",
    "Purchase Receipt": "public/js/ai_item_search.js",
    "Purchase Invoice": "public/js/ai_item_search.js",
    "Stock Entry": "public/js/ai_item_search.js",
    "Material Request": "public/js/ai_item_search.js"
}

doc_events = {
    "Item": {
        "after_insert": "ai_search.utils.sync_item",
        "on_update": "ai_search.utils.sync_item"
    }
}
