app_name = "ai_search"
app_title = "AI Search"
app_publisher = "ajmalajz"
app_description = "AI-powered semantic search for ERPNext"
app_email = "ajmalajz@gmail.com"
app_version = "1.0.0"
app_license = "MIT"

# Automatically reindex items
doc_events = {
    "Item": {
        "after_save": "ai_search.indexing.on_item_after_save",
        "on_trash": "ai_search.indexing.on_item_trash",
    }
}
