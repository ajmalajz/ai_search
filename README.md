
# AI Search for ERPNext (Arabic & English)

This app integrates Meilisearch with ERPNext for fuzzy, token-based search supporting Arabic and English.

## Installation
1. Upload this repo to GitHub.
2. In Frappe Cloud → Apps → Add App → Public GitHub App → Enter repo URL.
3. Add to `site_config.json`:
```json
{
  "meili_url": "https://YOUR-MEILI-HOST",
  "meili_api_key": "YOUR_API_KEY"
}
```
4. Initialize index:
```python
frappe.call('ai_search.api.setup_index')
frappe.call('ai_search.api.bulk_sync_items')
```
