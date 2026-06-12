from frappe.model.document import Document


class WoodDeliveryNote(Document):
    def validate(self):
        if not self.warehouse:
            self.warehouse = "Wood Store - EGL"