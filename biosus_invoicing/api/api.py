import frappe
from frappe.utils import get_url_to_form

def notify_po_creator(doc, event):
    """
    Sends a notification to the PO creator whenever a Purchase Receipt is submitted.
    Flags missing or damaged items if detected, otherwise sends a confirmation.
    """

    if not doc.purchase_order:
        return

    po = frappe.get_doc("Purchase Order", doc.purchase_order)
    issues = []

    # Generate URLs
    po_url = get_url_to_form("Purchase Order", po.name)
    pr_url = get_url_to_form("Purchase Receipt", doc.name)

    # Map PR items by item_code
    pr_map = {item.item_code: item for item in doc.items}

    # 1. Damaged items (rejected_qty field exists on Purchase Receipt Item)
    for pr_item in doc.items:
        if pr_item.rejected_qty and pr_item.rejected_qty > 0:
            issues.append(f"{pr_item.item_code}: {pr_item.rejected_qty} rejected (damaged)")

    # 2. Missing/partial items (compare against PO)
    for po_item in po.items:
        pr_item = pr_map.get(po_item.item_code)
        if not pr_item:
            issues.append(
                f"{po_item.item_code}: missing completely (ordered {po_item.qty})"
            )
        else:
            received = (pr_item.qty or 0) + (pr_item.rejected_qty or 0)
            if received < po_item.qty:
                missing = po_item.qty - received
                issues.append(
                    f"{po_item.item_code}: {missing} missing "
                    f"(ordered {po_item.qty}, received {received})"
                )

    # 3. Message body
    if issues:
        issues_html = "".join([f"<li>{i}</li>" for i in issues])
        msg = f"""
        <p>Purchase Receipt <a href="{pr_url}"><b>{doc.name}</b></a> 
        was submitted against Purchase Order <a href="{po_url}"><b>{po.name}</b>.</p>

        <p><b>Issues detected:</b></p>
        <ul>{issues_html}</ul>
        """
    else:
        msg = f"""
        <p>Purchase Receipt <a href="{pr_url}"><b>{doc.name}</b></a> 
        was submitted against Purchase Order <a href="{po_url}"><b>{po.name}</b>.</p>

        <p><b>All items received in full and in good condition ✔</b></p>
        """

    frappe.sendmail(
        recipients=[po.owner],
        subject=f"Purchase Receipt {doc.name} for PO {po.name}",
        message=msg
    )

def set_purchase_order_field(doc, event):
    if not doc.purchase_order and doc.items:
        first_po = next((i.purchase_order for i in doc.items if i.purchase_order), None)
        if first_po:
            doc.purchase_order = first_po
