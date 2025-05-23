frappe.ui.form.on('Quotation', {
    refresh: function(frm) {
        if (frm.doc.docstatus === 1 && frm.doc.status === "Open") {
            frm.add_custom_button("Generate Sales Order (Milestones)", function() {
                frappe.call({
                    method: "biosus_invoicing.api.quotation_utils.create_sales_order_from_quotation",
                    args: { quotation_name: frm.doc.name },
                    callback: function(r) {
                        if (r.message) {
                            frappe.msgprint("Sales Order created: " + r.message);
                            frappe.set_route("Form", "Sales Order", r.message);
                        }
                    }
                });
            });
        }
    }
});

