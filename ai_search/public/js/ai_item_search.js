
(function() {
    function set_query_item(frm) {
        frm.set_query('item_code', 'items', function() {
            return { query: 'ai_search.api.link_search_items' };
        });
    }
    const doctypes = ['Sales Invoice','Sales Order','Purchase Order','Delivery Note','Purchase Receipt','Purchase Invoice','Stock Entry','Material Request'];
    doctypes.forEach(dt => {
        frappe.ui.form.on(dt, { setup: set_query_item, refresh: set_query_item });
    });
})();
