// your_custom_app/public/js/quick_entry_grid.js

/**
 * A reusable function to configure an items table for "quick entry" mode.
 * This function hides item-specific fields and shows description/accounting fields.
 * It also automates setting the item_code to 'ONEOFF' for new rows.
 * @param {object} frm - The form object from the frappe.ui.form.on trigger.
 */
var setup_quick_entry_grid = function(frm) {
    const child_table_fieldname = 'items';
    const grid = frm.get_field(child_table_fieldname).grid;

    // Wait until the grid is fully rendered before making changes.
    if (!grid.grid_rows) {
        return;
    }

    // --- 1. DEFINE WHICH COLUMNS TO SHOW AND HIDE ---
    // These are the fields from your screenshot you want to see.
    const fields_to_show = [
        'description',
        'qty',
        'uom',
        'expense_account', // Use 'income_account' for sales docs if needed
        'item_tax_template',
        'rate',
        'amount'
    ];

    // These are the fields we want to remove from the view.
    const fields_to_hide = [
        'item_code',
        'item_name'
        // Add any other fields you want to hide, e.g., 'stock_uom'
    ];

    // --- 2. APPLY THE COLUMN VISIBILITY ---
    // This is the modern, recommended API for controlling grid columns.
    fields_to_show.forEach(field => {
        grid.update_docfield_property(field, 'hidden', 0); // 0 means not hidden
        grid.update_docfield_property(field, 'in_list_view', 1);
    });

    fields_to_hide.forEach(field => {
        grid.update_docfield_property(field, 'hidden', 1); // 1 means hidden
    });
    
    // Optional: Adjust column widths for a better layout
    grid.update_docfield_property('description', 'width', '300');


    // --- 3. AUTOMATE DATA ENTRY (Your existing logic, improved) ---
    // This event fires whenever a user clicks "Add Row".
    frm.cscript.on(child_table_fieldname + '_add', function(doc, cdt, cdn) {
        // Use frappe.model.set_value - it's the standard way to set data
        // and trigger any dependent field calculations.
        frappe.model.set_value(cdt, cdn, 'item_code', 'ONEOFF');
        // Setting item_code usually triggers item_name, uom, etc. to be fetched automatically.
        
        // Optional: Set focus to the description field for fast typing
        setTimeout(() => {
            const row = grid.get_row(cdn);
            if (row) {
                row.toggle_view(true, () => row.activate_field('description'));
            }
        }, 300); // A small delay ensures the row is ready.
    });

    // Refresh the grid to make sure all changes are visible
    grid.refresh();
};


// --- 4. ATTACH THE GLOBAL FUNCTION TO ALL RELEVANT DOCTYPES ---
// This clean loop makes the script easy to manage and extend.
const target_doctypes = [
    'Purchase Order',
    'Quotation',
    'Sales Order',
    'Sales Invoice',
    'Purchase Invoice',
    'Delivery Note',
    'Purchase Receipt'
];

target_doctypes.forEach(doctype => {
    frappe.ui.form.on(doctype, {
        // 'refresh' is a reliable trigger that runs when the form loads or is re-rendered.
        refresh: function(frm) {
            setup_quick_entry_grid(frm);
        },
        // We can also re-apply it if the items table is refreshed for any other reason
        items_on_form_rendered: function(frm) {
            setup_quick_entry_grid(frm);
        }
    });
});