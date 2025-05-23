# biosus_invoicing/biosus_invoicing/api/quotation.py

import frappe
from frappe.utils import flt

MILESTONES = [
    {"code": "PROJECT-DEPOSIT", "desc": "Deposit", "percent": 50},
    {"code": "PROJECT-INSTALL", "desc": "Install", "percent": 40},
    {"code": "PROJECT-COMMISSIONING", "desc": "Commissioning", "percent": 10},
]

@frappe.whitelist()
def create_sales_order_from_quotation(quotation_name):
    """
    API method: Create a Sales Order from the given Quotation with milestone line items.
    Returns Sales Order name if successful.
    """

    quotation = frappe.get_doc("Quotation", quotation_name)

    if quotation.docstatus != 1:
        frappe.throw(f"Quotation {quotation_name} must be submitted before creating Sales Order.")

    total_amount = flt(quotation.net_total)

    if total_amount <= 0:
        frappe.throw("Quotation total amount must be positive.")

    so_items = []
    for milestone in MILESTONES:
        amount = flt(total_amount * milestone["percent"] / 100, 2)
        so_items.append({
            "item_code": milestone["code"],
            "item_name": milestone["desc"],
            "description": milestone["desc"],
            "qty": 1,
            "rate": amount,
            "amount": amount,
            "uom": "Nos",
            "conversion_factor": 1,
        })

    so = frappe.get_doc({
        "doctype": "Sales Order",
        "customer": quotation.party_name,
        "transaction_date": frappe.utils.nowdate(),
        "delivery_date": frappe.utils.nowdate(),
        "company": quotation.company,
        "currency": quotation.currency,
        "quotation": quotation_name,
        "items": so_items,
    })

    so.insert()
    # Optional: so.submit() if you want it auto-submitted
    # For now, leave as Draft so user can review
    frappe.db.commit()

    quotation.db_set("status", "Ordered")
    frappe.db.commit()

    return so.name
