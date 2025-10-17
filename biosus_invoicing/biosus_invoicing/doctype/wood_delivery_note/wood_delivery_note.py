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
    
    def on_cancel(self):
        """Cancel linked stock entry"""
        self.cancel_stock_entry()
    
    def create_stock_entry(self):
        """Create Material Receipt for wood delivery"""
        
        # Map wood type to item code
        item_mapping = {
            "Standard Wood": "WOOD-STD",
            "Waste Wood": "WOOD-WASTE",
            "FSC Certified": "WOOD-FSC"
        }
        
        item_code = item_mapping.get(self.wood_type, "WOOD-STD")
        
        # Convert kg to tonnes
        qty_in_tonnes = self.net_weight_kg / 1000
        
        # Create Stock Entry
        stock_entry = frappe.get_doc({
            "doctype": "Stock Entry",
            "stock_entry_type": "Material Receipt",
            "to_warehouse": self.warehouse,
            "items": [{
                "item_code": item_code,
                "qty": qty_in_tonnes,
                "uom": "Tonne",
                "t_warehouse": self.warehouse,
                "basic_rate": 0  # Price can be updated from PO if linked
            }],
            "remarks": f"Wood delivery from {self.supplier} - Ticket #{self.ticket_number}"
        })
        
        stock_entry.insert(ignore_permissions=True)
        stock_entry.submit()
        
        # Link back to this delivery note
        self.db_set("stock_entry", stock_entry.name)
        
        frappe.msgprint(f"Stock Entry {stock_entry.name} created successfully")
    
    def cancel_stock_entry(self):
        """Cancel the linked stock entry"""
        if self.stock_entry:
            stock_entry = frappe.get_doc("Stock Entry", self.stock_entry)
            if stock_entry.docstatus == 1:
                stock_entry.cancel()
                frappe.msgprint(f"Stock Entry {self.stock_entry} cancelled")
