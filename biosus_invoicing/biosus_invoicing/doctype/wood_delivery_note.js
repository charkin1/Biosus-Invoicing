frappe.ui.form.on('Wood Delivery Note', {
    refresh: function(frm) {
        // Show link to stock entry if exists
        if (frm.doc.stock_entry) {
            frm.add_custom_button(__('View Stock Entry'), function() {
                frappe.set_route('Form', 'Stock Entry', frm.doc.stock_entry);
            });
        }
        
        // Show link to PO if exists
        if (frm.doc.reference_po) {
            frm.add_custom_button(__('View Purchase Order'), function() {
                frappe.set_route('Form', 'Purchase Order', frm.doc.reference_po);
            });
        }
    },
    
    supplier: function(frm) {
        // Auto-fetch any open POs for this supplier (optional)
        if (frm.doc.supplier) {
            frappe.call({
                method: 'frappe.client.get_list',
                args: {
                    doctype: 'Purchase Order',
                    filters: {
                        supplier: frm.doc.supplier,
                        docstatus: 1,
                        status: ['!=', 'Closed']
                    },
                    fields: ['name'],
                    limit: 1
                },
                callback: function(r) {
                    if (r.message && r.message.length > 0) {
                        frm.set_value('reference_po', r.message[0].name);
                    }
                }
            });
        }
    }
});
