import frappe
from frappe.model.document import Document


class WoodSalesNote(Document):
    def validate(self):
        """Validation before save."""
        if not self.warehouse:
            self.warehouse = "Wood Store - EGL"

        if not self.supplier:
            self.supplier = "ECOGENESIS"

    def on_submit(self):
        """Create stock entry when sales note is submitted."""
        self.create_stock_entry()

    def on_cancel(self):
        """Cancel linked stock entry when sales note is cancelled."""
        self.cancel_stock_entry()

    def create_stock_entry(self):
        item_mapping = {
            "LOGS": "WOOD-LOGS",
            "CHIP LOGS": "WOOD-CHIP-LOGS",

            # Legacy fallbacks in case old values are ever copied/amended in.
            "Standard Wood": "WOOD-STD",
            "Waste Wood": "WOOD-WASTE",
            "FSC Certified": "WOOD-FSC",
        }

        item_code = item_mapping.get(self.wood_type)

        if not item_code:
            frappe.throw(
                f"No Item mapping configured for Wood Type: {self.wood_type or '[blank]'}"
            )

        stock_entry = frappe.get_doc({
            "doctype": "Stock Entry",
            "stock_entry_type": "Material Issue",
            "company": "Ecogenesis Ltd",
            "items": [{
                "item_code": item_code,
                "qty": self.net_weight_kg,
                "uom": "Kg",
                "s_warehouse": self.warehouse,
                "basic_rate": 0,
            }],
            "remarks": (
                f"Wood sale to {self.customer} "
                f"- Ticket #{self.ticket_number}"
            ),
        })

        stock_entry.insert(ignore_permissions=True)
        stock_entry.submit()

        self.db_set("stock_entry", stock_entry.name)
        frappe.msgprint(f"Stock Entry {stock_entry.name} created successfully")

    def cancel_stock_entry(self):
        """Cancel the linked stock entry."""
        if self.stock_entry:
            stock_entry = frappe.get_doc("Stock Entry", self.stock_entry)
            if stock_entry.docstatus == 1:
                stock_entry.cancel()
                frappe.msgprint(f"Stock Entry {self.stock_entry} cancelled")
