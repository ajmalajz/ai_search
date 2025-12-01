
// AI Search: override Link field query for item_code in grid rows
(function() {
    function set_query_item(frm) {
        try {
            frm.set_query('item_code', 'items', function(doc, cdt, cdn) {
                return {
                    query: 'ai_search.api.link_search_items',
                    filters: {}
                };
            });
        } catch (e) {
            console && console.warn('ai_search set_query failed', e);
        }
    }

    function bind(frm) { set_query_item(frm); }

    const doctypes = [
        'Sales Invoice','Sales Order','Purchase Order','Delivery Note',
        'Purchase Receipt','Purchase Invoice','Stock Entry','Material Request'
    ];

    doctypes.forEach(dt => {
        frappe.ui.form.on(dt, {
            setup: bind,
            refresh: bind,
            onload: bind
        });
    });
})();
