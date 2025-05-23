import frappe
from frappe import _

@frappe.whitelist()
def test_api():
    return {"message": "API is working!"}
