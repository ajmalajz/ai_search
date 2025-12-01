app_name = 'ai_search'
app_title = 'AI Search'
app_publisher = 'Your Name'
app_description = 'Custom search engine for ERPNext using SQLite'
app_email = 'you@example.com'
app_license = 'MIT'

# Override search
override_whitelisted_methods = {
    'frappe.desk.search.search_link': 'ai_search.search.custom_search'
}
