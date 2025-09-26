// your_custom_app/public/js/quick_entry_grid.js

// This function uses jQuery to directly manipulate the grid's HTML.
// It's a "brute force" method to override everything else.
var force_layout_with_jquery = function(frm) {
    console.log("[JQUERY SCRIPT] Forcing layout via direct DOM manipulation...");

    const grid_wrapper = $(frm.get_field('items').wrapper);
    if (grid_wrapper.length === 0) {
        console.log("[JQUERY SCRIPT] Grid wrapper not found. Aborting.");
        return;
    }

    // --- 1. THE DEFINITIVE LIST OF COLUMNS WE WANT TO SEE ---
    const visible_columns = {
        'description': '400px', // Note: adding 'px' for CSS
        'qty':         '100px',
        'rate':        '120px',
        'amount':      '120px'
    };

    // --- 2. HIDE ALL COLUMNS FIRST ---
    // Hide all header cells and data cells in the grid.
    grid_wrapper.find('.grid-heading-row .grid-header-cell').hide();
    grid_wrapper.find('.grid-row .grid-cell').hide();
    console.log("[JQUERY SCRIPT] All columns hidden.");

    // --- 3. SHOW ONLY THE COLUMNS WE WANT AND SET THEIR WIDTHS ---
    for (const fieldname in visible_columns) {
        const width = visible_columns[fieldname];

        // Find the header for this fieldname and show it
        const header_cell = grid_wrapper.find(`.grid-heading-row .grid-header-cell[data-fieldname="${fieldname}"]`);
        header_cell.show();
        header_cell.css('width', width);

        // Find all data cells for this fieldname and show them
        const data_cells = grid_wrapper.find(`.grid-row .grid-cell[data-fieldname="${fieldname}"]`);
        data_cells.show();
    }
    
    console.log("[JQUERY SCRIPT] Whitelisted columns have been made visible and resized.");
};


// --- THIS PART ATTACHES OUR FUNCTIONS ---
const apply_quick_entry_logic = function(doctype) {
    frappe.ui.form.on(doctype, {
        refresh: function(frm) {
            // Run our forceful script after a 1-second delay to ensure
            // all of Frappe's own rendering scripts have finished.
            setTimeout(() => {
                force_layout_with_jquery(frm);
            }, 1000); // 1-second delay
        }
    });

    // The ONEOFF logic is separate and should still work.
    frappe.ui.form.on(doctype + ' Item', {
        items_add: function(frm, cdt, cdn) {
            console.log("[JQUERY SCRIPT] Setting item_code to ONEOFF.");
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