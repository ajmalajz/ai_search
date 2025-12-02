app_name = 'ai_search'
app_title = 'AI Search'
app_publisher = 'Your Name'
app_description = 'Custom search engine override for ERPNext link search'
app_email = 'you@example.com'
app_license = 'MIT'

# IMPORTANT: Frappe Cloud validates hooks.py presence inside the package folder

override_whitelisted_methods = {
    'frappe.desk.search.search_link': 'ai_search.search.custom_search'
}
