// your_custom_app/public/js/quick_entry_grid.js

var setup_quick_entry_grid = function(frm) {
    console.log("[METADATA SCRIPT] Attempting to enforce layout...");

    const grid = frm.get_field('items').grid;
    if (!grid) {
        return; // Grid controller not ready
    }

    // --- 1. THE DEFINITIVE LIST OF COLUMNS WE WANT TO SEE ---
    const visible_columns = {
        'description': '400',
        'qty':         '100',
        'rate':        '120',
        'amount':      '120'
    };

    // --- 2. THE ROBUST SOLUTION: GET FIELDS FROM METADATA ---
    // Get the name of the child doctype (e.g., "Purchase Order Item")
    const child_doctype = frm.fields_dict.items.df.options;
    // Get all field definitions for that doctype directly from the metadata cache
    const all_docfields = frappe.meta.get_docfields(child_doctype);
    // Extract just the fieldnames into a simple array
    const all_fieldnames = all_docfields.map(df => df.fieldname);

    console.log(`[METADATA SCRIPT] Enforcing layout for ${child_doctype}. Visible fields will be:`, Object.keys(visible_columns));

    // --- 3. LOOP THROUGH EVERY FIELD AND FORCE VISIBILITY ---
    all_fieldnames.forEach(fieldname => {
        // Is this field in our list of columns to show?
        if (fieldname in visible_columns) {
            // YES: Make it visible and set its width.
            grid.update_docfield_property(fieldname, 'hidden', 0);
            grid.update_docfield_property(fieldname, 'in_list_view', 1);
            grid.update_docfield_property(fieldname, 'width', visible_columns[fieldname]);
        } else {
            // NO: Hide it. No exceptions.
            grid.update_docfield_property(fieldname, 'hidden', 1);
        }
    });

    grid.refresh();
    console.log("[METADATA SCRIPT] Layout enforced.");
};

// --- THIS PART IS ALREADY WORKING AND DOES NOT NEED TO CHANGE ---
// It correctly attaches the function and handles the 'ONEOFF' logic.
const apply_quick_entry_logic = function(doctype) {
    frappe.ui.form.on(doctype, {
        // items_on_form_rendered is more reliable than refresh for grids
        items_on_form_rendered: function(frm) {
            setup_quick_entry_grid(frm);
        },
        refresh: function(frm) {
            // Keep a short delay as a fallback
            setTimeout(() => {
                setup_quick_entry_grid(frm);
            }, 200);
        }
    });

    frappe.ui.form.on(doctype + ' Item', {
        items_add: function(frm, cdt, cdn) {
            console.log("[METADATA SCRIPT] Setting item_code to ONEOFF.");
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