
# AI Search (Meilisearch) for ERPNext — Arabic & English

**Repository layout must keep `setup.py` and/or `pyproject.toml` at the repository root.** Push this folder to GitHub as-is.

## Configure
Add to `site_config.json`:
```json
{
  "meili_url": "https://YOUR-MEILI-HOST",
  "meili_api_key": "YOUR_API_KEY"
}
```

## Initialize
```python
frappe.call('ai_search.api.setup_index')
frappe.call('ai_search.api.bulk_sync_items', {'batch_size': 1000})
```
