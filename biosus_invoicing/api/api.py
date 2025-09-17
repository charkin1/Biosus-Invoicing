python
import frappe
from frappe.utils import get_url_to_form

def notify_po_creator(doc, event):
    """
    Sends a notification to the PO creator whenever a Delivery Note is submitted.
    Includes links to the DN and PO, and flags issues if detected.
    """

    if not doc.purchase_order:
        return

    po = frappe.get_doc("Purchase Order", doc.purchase_order)
    issues = []

    # Generate URLs to PO and DN forms
    po_url = get_url_to_form("Purchase Order", po.name)
    dn_url = get_url_to_form("Delivery Note", doc.name)

    # Map DN items by item_code for quick lookup
    dn_map = {item.item_code: item for item in doc.items}

    # 1. Damaged check (rejected_qty)
    for dn_item in doc.items:
        if dn_item.rejected_qty and dn_item.rejected_qty > 0:
            issues.append(f"{dn_item.item_code}: {dn_item.rejected_qty} damaged")

    # 2. Missing or partial items vs PO
    for po_item in po.items:
        dn_item = dn_map.get(po_item.item_code)
        if not dn_item:
            issues.append(
                f"{po_item.item_code}: missing completely (ordered {po_item.qty})"
            )
        else:
            delivered = (dn_item.qty or 0) + (dn_item.rejected_qty or 0)
            if delivered < po_item.qty:
                missing = po_item.qty - delivered
                issues.append(
                    f"{po_item.item_code}: {missing} missing "
                    f"(ordered {po_item.qty}, delivered {delivered})"
                )

    # 3. Compose message
    if issues:
        issues_html = "".join([f"<li>{i}</li>" for i in issues])
        msg = f"""
        <p>Delivery Note <a href="{dn_url}"><b>{doc.name}</b></a> has been submitted against 
        Purchase Order <a href="{po_url}"><b>{po.name}</b></a>.</p>

        <p><b>Issues detected:</b></p>
        <ul>{issues_html}</ul>
        """
    else:
        msg = f"""
        <p>Delivery Note <a href="{dn_url}"><b>{doc.name}</b></a> has been submitted against 
        Purchase Order <a href="{po_url}"><b>{po.name}</b></a>.</p>

        <p><b>All items delivered in full and in good condition ✔</b></p>
        """

    # 4. Send the email
    frappe.sendmail(
        recipients=[po.owner],
        subject=f"Delivery Note {doc.name} for PO {po.name}",
        message=msg
    )
