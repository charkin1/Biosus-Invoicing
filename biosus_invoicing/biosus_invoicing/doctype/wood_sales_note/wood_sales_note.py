from frappe.model.document import Document


class WoodSalesNote(Document):
    def validate(self):
        if not self.warehouse:
            self.warehouse = "Wood Store - EGL"

        if not self.supplier:
            self.supplier = "ECOGENESIS"