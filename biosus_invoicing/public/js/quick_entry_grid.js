// your_custom_app/public/js/quick_entry_grid.js

var setup_quick_entry_grid = function(frm) {
    console.log("[FORCEFUL SCRIPT] Attempting to enforce layout...");

    const grid = frm.get_field('items').grid;
    if (!grid || !grid.grid_rows || grid.grid_rows.length === 0) {
        return; // Grid not ready
    }

    // --- 1. THIS IS THE KEY: A definitive list of columns we want to see ---
    // The script will hide EVERYTHING else.
    const visible_columns = {
        'description': '400',
        'qty':         '100',
        'rate':        '120',
        'amount':      '120'
    };

    // --- 2. GET ALL POSSIBLE FIELDS FOR THE GRID ---
    const all_fields = Object.keys(grid.grid_rows[0].grid_form.fields_dict);

    console.log("[FORCEFUL SCRIPT] Enforcing layout. Visible fields will be:", Object.keys(visible_columns));

    // --- 3. LOOP THROUGH EVERY FIELD AND FORCE VISIBILITY ---
    all_fields.forEach(fieldname => {
        // Is this field in our list of columns to show?
        if (fieldname in visible_columns) {
            // YES: Make it visible and set its width.
            grid.update_docfield_property(fieldname, 'hidden', 0);
            grid.update_docfield_property(fieldname, 'in_list_view', 1); // Extra forceful command
            grid.update_docfield_property(fieldname, 'width', visible_columns[fieldname]);
        } else {
            // NO: Hide it. No exceptions.
            grid.update_docfield_property(fieldname, 'hidden', 1);
        }
    });

    grid.refresh();
    console.log("[FORCEFUL SCRIPT] Layout enforced.");
};

// --- THIS PART IS ALREADY WORKING AND DOES NOT NEED TO CHANGE ---
// It correctly attaches the function and handles the 'ONEOFF' logic.
const apply_quick_entry_logic = function(doctype) {
    frappe.ui.form.on(doctype, {
        items_on_form_rendered: function(frm) {
            setup_quick_entry_grid(frm);
        },
        refresh: function(frm) {
            setTimeout(() => {
                setup_quick_entry_grid(frm);
            }, 500);
        }
    });

    frappe.ui.form.on(doctype + ' Item', {
        items_add: function(frm, cdt, cdn) {
            console.log("[FORCEFUL SCRIPT] Setting item_code to ONEOFF.");
            frappe.model.set_value(cdt, cdn, 'item_code', 'ONEOFF');
        }
    });
};

const target_doctypes = [
    'Purchase Order', 'Quotation', 'Sales Order', 'Sales Invoice',
    'Purchase Invoice', 'Delivery Note', 'Purchase Receipt'
];
target_doctypes.forEach(doctype => {
    apply_quick_entry_logic(doctype);
});