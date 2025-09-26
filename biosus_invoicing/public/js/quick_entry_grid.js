// your_custom_app/public/js/quick_entry_grid.js

var setup_quick_entry_grid = function(frm) {
    console.log("Attempting to set up quick entry grid..."); // DEBUG LOG 1

    const child_table_fieldname = 'items';
    const grid = frm.get_field(child_table_fieldname).grid;

    // VERY IMPORTANT CHECK: Exit if the grid or its internal 'grid_rows' array doesn't exist yet.
    if (!grid || !grid.grid_rows) {
        console.log("Grid is not ready yet. Aborting."); // DEBUG LOG 2
        return;
    }

    console.log("Grid is ready. Applying custom layout..."); // DEBUG LOG 3

    // --- 1. DEFINE COLUMN LAYOUT ---
    const column_layout = {
        'description':       { hidden: 0, width: '350' },
        'qty':               { hidden: 0, width: '100' },
        'uom':               { hidden: 0, width: '120' },
        'expense_account':   { hidden: 0, width: '200' },
        'item_tax_template': { hidden: 0, width: '200' },
        'rate':              { hidden: 0, width: '120' },
        'amount':            { hidden: 0, width: '120' },
        'item_code':         { hidden: 1 },
        'item_name':         { hidden: 1 }
    };

    // --- 2. APPLY THE LAYOUT ---
    for (const fieldname in column_layout) {
        const props = column_layout[fieldname];
        grid.update_docfield_property(fieldname, 'hidden', props.hidden);
        if (props.hidden === 0 && props.width) {
            grid.update_docfield_property(fieldname, 'width', props.width);
        }
    }

    // --- 3. AUTOMATE DATA ENTRY (No changes here) ---
    frm.cscript.on(child_table_fieldname + '_add', function(doc, cdt, cdn) {
        frappe.model.set_value(cdt, cdn, 'item_code', 'ONEOFF');
    });

    // --- 4. REFRESH THE GRID ---
    grid.refresh();
    console.log("Grid layout applied and refreshed."); // DEBUG LOG 4
};


// --- ATTACH THE GLOBAL FUNCTION TO ALL RELEVANT DOCTYPES ---
const target_doctypes = [
    'Purchase Order', 'Quotation', 'Sales Order', 'Sales Invoice', 
    'Purchase Invoice', 'Delivery Note', 'Purchase Receipt'
];

target_doctypes.forEach(doctype => {
    frappe.ui.form.on(doctype, {
        // This is a more specific and reliable trigger for child tables.
        // It fires after the 'items' table is fully rendered on the form.
        items_on_form_rendered: function(frm) {
            setup_quick_entry_grid(frm);
        },
        // 'refresh' is still a good fallback for initial load.
        refresh: function(frm) {
            // A small delay can give the grid component time to initialize.
            setTimeout(() => {
                setup_quick_entry_grid(frm);
            }, 500); // Increased timeout to 500ms for more reliability
        }
    });
});