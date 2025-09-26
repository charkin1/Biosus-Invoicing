// your_custom_app/public/js/quick_entry_grid.js

var setup_quick_entry_grid = function(frm) {
    console.log("Attempting to set up quick entry grid...");

    const child_table_fieldname = 'items';
    const grid = frm.get_field(child_table_fieldname).grid;

    if (!grid || !grid.grid_rows) {
        console.log("Grid is not ready yet. Aborting.");
        return;
    }

    console.log("Grid is ready. Applying custom layout...");

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
    
    // --- 4. REFRESH THE GRID ---
    grid.refresh();
    console.log("Grid layout applied and refreshed.");
};


// --- ATTACH THE GLOBAL FUNCTION AND DATA AUTOMATION ---
// We will define the data automation part outside the main function
// for compatibility with older Frappe versions.

const apply_quick_entry_logic = function(doctype) {
    frappe.ui.form.on(doctype, {
        // This is a reliable trigger for child tables.
        items_on_form_rendered: function(frm) {
            setup_quick_entry_grid(frm);
        },
        // 'refresh' is still a good fallback for initial load.
        refresh: function(frm) {
            setTimeout(() => {
                setup_quick_entry_grid(frm);
            }, 500);
        }
    });

    // --- 3. AUTOMATE DATA ENTRY (OLDER, COMPATIBLE SYNTAX) ---
    // This event fires when a new row is added to the "items" table.
    // The event name is constructed by combining the child DocType name with "_add".
    // Example: "Purchase Order Item_add"
    frappe.ui.form.on(doctype + ' Item', {
        items_add: function(frm, cdt, cdn) {
            console.log("New item row added, setting item_code to ONEOFF.");
            frappe.model.set_value(cdt, cdn, 'item_code', 'ONEOFF');
        }
    });
};


// --- APPLY THE LOGIC TO ALL RELEVANT DOCTYPES ---
const target_doctypes = [
    'Purchase Order', 'Quotation', 'Sales Order', 'Sales Invoice', 
    'Purchase Invoice', 'Delivery Note', 'Purchase Receipt'
];

target_doctypes.forEach(doctype => {
    apply_quick_entry_logic(doctype);
});