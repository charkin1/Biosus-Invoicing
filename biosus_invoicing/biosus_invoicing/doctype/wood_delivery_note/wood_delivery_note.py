import frappe
from frappe.model.document import Document

class WoodDeliveryNote(Document):
    def validate(self):
        """Validation before save"""
        if not self.warehouse:
            self.warehouse = "Ecogenesis - Wood Store"
    
    def on_submit(self):
        """Create stock entry when delivery note is submitted"""
        self.create_stock_entry()
    
    def create_stock_entry(self):
        item_mapping = {
            "Standard Wood": "WOOD-STD",
            "Waste Wood": "WOOD-WASTE",
            "FSC Certified": "WOOD-FSC"
        }

        item_code = item_mapping.get(self.wood_type, "WOOD-STD")

        stock_entry = frappe.get_doc({
            "doctype": "Stock Entry",
            "stock_entry_type": "Material Receipt",
            "company": "Ecogenesis Ltd",  # CRITICAL
            "items": [{
                "item_code": item_code,
                "qty": self.net_weight_kg,
                "uom": "Kg",
                "t_warehouse": self.warehouse,
                "basic_rate": 0
            }],
            "remarks": f"Wood delivery from {self.supplier} - Ticket #{self.ticket_number}"
        })

        stock_entry.insert(ignore_permissions=True)
        stock_entry.submit()

        self.db_set("stock_entry", stock_entry.name)
        
        frappe.msgprint(f"Stock Entry {stock_entry.name} created successfully")
    
    def cancel_stock_entry(self):
        """Cancel the linked stock entry"""
        if self.stock_entry:
            stock_entry = frappe.get_doc("Stock Entry", self.stock_entry)
            if stock_entry.docstatus == 1:
                stock_entry.cancel()
                frappe.msgprint(f"Stock Entry {self.stock_entry} cancelled")
