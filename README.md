# ai_search

Custom Frappe app to override ERPNext link field search using SQLite-based fuzzy search.

## Installation Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/ajmalajz/ai_search.git
   ```

2. Navigate to the app directory:
   ```bash
   cd ai_search
   ```

3. Install the app on your Frappe/ERPNext site:
   ```bash
   bench get-app https://github.com/ajmalajz/ai_search.git
   bench --site your-site-name install-app ai_search
   bench migrate
   ```

4. Restart bench:
   ```bash
   bench restart
   ```

After installation, link field searches will use the custom fuzzy search logic.
