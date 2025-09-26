// your_custom_app/public/js/quick_entry_grid.js

// A reusable function to set up the quick entry grid
var setup_quick_entry_grid = function(frm) {
    // This is the fieldname of the child table in the parent DocType (e.g., 'items')
    let child_table_fieldname = 'items';

    // --- 1. HIDE UNNECESSARY COLUMNS IN THE GRID ---
    // This uses the official Frappe API to modify the grid's properties.
    // It's better than trying to manipulate the DOM with jQuery directly.
    let fields_to_hide = ['item_code', 'item_name', 'stock_uom', 'rate', 'amount'];
    fields_to_hide.forEach(field => {
        frm.get_field(child_table_fieldname).grid.update_docfield_property(field, 'hidden', 1);
    });

    // You can also make other columns wider to fill the space
    frm.get_field(child_table_fieldname).grid.update_docfield_property('description', 'width', '400');


    // --- 2. AUTOMATE DATA ENTRY WHEN A NEW ROW IS ADDED ---
    // This is the magic that makes it "quick entry".
    // When a user clicks "Add Row", this code will run.
    frm.cscript.on(child_table_fieldname + '_add', function(doc, cdt, cdn) {
        let row = locals[cdt][cdn];
        
        // Automatically set the Item Code to 'ONEOFF' in the background.
        // This is crucial because the field is still required by the backend,
        // even if it's hidden from the user.
        frappe.model.set_value(cdt, cdn, 'item_code', 'ONEOFF');

        // You can set other default values here if needed
        // For example, set a default rate of 1 so the user only enters the total amount.
        frappe.model.set_value(cdt, cdn, 'rate', 1);
        
        // Optional: Set focus to the description field for fast typing
        setTimeout(() => {
            const grid = frm.get_field(child_table_fieldname).grid;
            const rowIndex = grid.get_row_index(cdn);
            grid.grid_rows[rowIndex-1].activate_field('description');
        }, 100);
    });

    // Refresh the grid to apply the changes
    frm.get_field(child_table_fieldname).grid.refresh();
};


// --- 3. ATTACH THE FUNCTION TO THE PARENT DOCTYPE ---
// We hook into the 'refresh' trigger of the main form.
// This ensures our customizations are applied whenever the form loads or is refreshed.
frappe.ui.form.on('Sales Order', {
    refresh: function(frm) {
        setup_quick_entry_grid(frm);
    }
});

frappe.ui.form.on('Purchase Order', {
    refresh: function(frm) {
        setup_quick_entry_grid(frm);
    }
});

frappe.ui.form.on('Quotation', {
    refresh: function(frm) {
        setup_quick_entry_grid(frm);
    }
});

frappe.ui.form.on('Sales Invoice', {
    refresh: function(frm) {
        setup_quick_entry_grid(frm);
    }
});

// ... Add more for Purchase Invoice, Delivery Note, etc.