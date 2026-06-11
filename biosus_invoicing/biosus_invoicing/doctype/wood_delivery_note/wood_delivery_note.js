frappe.ui.form.on('Wood Delivery Note', {
    refresh: function(frm) {
        if (!frm.is_new() && frm.doc.stock_entry) {
            frm.add_custom_button(__('View Stock Entry'), function() {
                frappe.set_route('Form', 'Stock Entry', frm.doc.stock_entry);
            });
        }

        if (!frm.is_new() && frm.doc.reference_po) {
            frm.add_custom_button(__('View Purchase Order'), function() {
                frappe.set_route('Form', 'Purchase Order', frm.doc.reference_po);
            });
        }
    },

    supplier: function(frm) {
        if (!frm.doc.supplier) {
            frm.set_value('reference_po', null);
            return;
        }

        // Do not overwrite a manually selected purchase order.
        if (frm.doc.reference_po) {
            return;
        }

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
                limit_page_length: 1,
                order_by: 'transaction_date desc'
            },
            callback: function(r) {
                if (r.message && r.message.length > 0 && !frm.doc.reference_po) {
                    frm.set_value('reference_po', r.message[0].name);
                }
            }
        });
    }
});