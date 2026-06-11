frappe.ui.form.on('Wood Sales Note', {
    refresh: function(frm) {
        if (!frm.is_new() && frm.doc.stock_entry) {
            frm.add_custom_button(__('View Stock Entry'), function() {
                frappe.set_route('Form', 'Stock Entry', frm.doc.stock_entry);
            });
        }

        if (!frm.is_new() && frm.doc.sales_invoice) {
            frm.add_custom_button(__('View Sales Invoice'), function() {
                frappe.set_route('Form', 'Sales Invoice', frm.doc.sales_invoice);
            });
        }
    }
});
