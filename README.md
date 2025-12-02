# ai_search

Frappe app to override ERPNext link search.

## Required structure
```
ai_search/
 ├─ setup.py
 ├─ MANIFEST.in
 ├─ requirements.txt
 ├─ README.md
 └─ ai_search/
     ├─ __init__.py
     ├─ hooks.py
     ├─ modules.txt
     ├─ search.py
     └─ doctype/
         └─ ai_search_index/
             ├─ __init__.py
             ├─ ai_search_index.json
             └─ ai_search_index.py
```
