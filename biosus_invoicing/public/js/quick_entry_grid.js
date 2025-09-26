// your_custom_app/public/js/quick_entry_grid.js

/**
 * A reusable function to configure an items table for "quick entry" mode.
 */
var setup_quick_entry_grid = function(frm) {
    const child_table_fieldname = 'items';
    const grid = frm.get_field(child_table_fieldname).grid;

    // Exit if the grid or its rows aren't ready yet.
    if (!grid.grid_rows) {
        return;
    }

    // --- 1. DEFINE COLUMN LAYOUT (VISIBILITY AND WIDTHS) ---
    // This gives you full control over the final appearance.
    // The width is in pixels. Adjust these values to your liking.
    const column_layout = {
        // Visible Columns
        'description':       { hidden: 0, width: '350' },
        'qty':               { hidden: 0, width: '100' },
        'uom':               { hidden: 0, width: '120' },
        'expense_account':   { hidden: 0, width: '200' }, // Use 'income_account' for sales docs
        'item_tax_template': { hidden: 0, width: '200' },
        'rate':              { hidden: 0, width: '120' },
        'amount':            { hidden: 0, width: '120' },

        // Hidden Columns
        'item_code':         { hidden: 1 },
        'item_name':         { hidden: 1 }
    };

    // --- 2. APPLY THE LAYOUT TO THE GRID ---
    // This loop iterates through your layout and applies the properties.
    for (const fieldname in column_layout) {
        const props = column_layout[fieldname];
        grid.update_docfield_property(fieldname, 'hidden', props.hidden);

        // Only set width if the column is not hidden
        if (props.hidden === 0 && props.width) {
            grid.update_docfield_property(fieldname, 'width', props.width);
        }
    }


    // --- 3. AUTOMATE DATA ENTRY ---
    // This part remains the same and ensures the 'ONEOFF' item is set automatically.
    frm.cscript.on(child_table_fieldname + '_add', function(doc, cdt, cdn) {
        frappe.model.set_value(cdt, cdn, 'item_code', 'ONEOFF');
        
        // Optional: Set focus to the description field
        setTimeout(() => {
            const row = grid.get_row(cdn);
            if (row) {
                // This opens the row for editing and focuses on the description field
                row.toggle_view(true, () => row.activate_field('description'));
            }
        }, 300);
    });

    // --- 4. REFRESH THE GRID ---
    // This is crucial. It tells the grid to redraw itself with the new properties.
    grid.refresh();
};


// --- ATTACH THE GLOBAL FUNCTION TO ALL RELEVANT DOCTYPES ---
// This section should already be in your file and doesn't need to change.
const target_doctypes = [
    'Purchase Order', 'Quotation', 'Sales Order', 'Sales Invoice', 
    'Purchase Invoice', 'Delivery Note', 'Purchase Receipt'
];

target_doctypes.forEach(doctype => {
    frappe.ui.form.on(doctype, {
        refresh: function(frm) {
            // Use a small timeout to ensure the grid is fully rendered before we modify it.
            // This is a robust way to handle timing issues.
            setTimeout(() => {
                setup_quick_entry_grid(frm);
            }, 200);
        },
        items_on_form_rendered: function(frm) {
            setup_quick_entry_grid(frm);
        }
    });
});