app_name = "ai_search"
app_title = "AI Search"
app_publisher = "ajmalajz"
app_description = "AI-powered semantic search for ERPNext"
app_email = "ajmalajz@example.com"
app_version = "1.0.0"
app_license = "MIT"

# Include JS overrides globally
app_include_js = [
    "ai_search/js/ai_search_client.js"
]

# Trigger reindexing on save/delete
doc_events = {
    "Item": {
        "after_save": "ai_search.indexing.on_item_after_save",
        "on_trash": "ai_search.indexing.on_item_trash",
    },
    "Customer": {
        "after_save": "ai_search.indexing.on_customer_after_save",
        "on_trash": "ai_search.indexing.on_customer_trash",
    },
    "Supplier": {
        "after_save": "ai_search.indexing.on_supplier_after_save",
        "on_trash": "ai_search.indexing.on_supplier_trash",
    },
}
