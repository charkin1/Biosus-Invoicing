import frappe
from frappe.utils import get_url_to_form
from frappe import _
import json

def notify_po_creator(doc, event):
    """
    Notify the PO creator whenever a Purchase Receipt is submitted.
    - Always send a message (issues or confirmation).
    - Attach the Purchase Order PDF.
    - If no email available for PO owner, do not block submission:
      warn the submitting user instead.
    """

    if not doc.custom_purchase_order:
        return

    po = frappe.get_doc("Purchase Order", doc.custom_purchase_order)
    issues = []

    # Generate URLs
    po_url = get_url_to_form("Purchase Order", po.name)
    pr_url = get_url_to_form("Purchase Receipt", doc.name)

    # Map PR items by item_code
    pr_map = {item.item_code: item for item in doc.items}

    # 1. Damaged items
    for pr_item in doc.items:
        if pr_item.rejected_qty and pr_item.rejected_qty > 0:
            issues.append(f"{pr_item.item_code}: {pr_item.rejected_qty} rejected (damaged)")

    # 2. Missing/partial items
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

    # 3. Build email message body
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

    # 4. Handle recipient email
    recipient_email = None
    try:
        po_owner_user = frappe.get_doc("User", po.owner)
        if po_owner_user.email:
            recipient_email = po_owner_user.email
    except Exception:
        pass

    if recipient_email:
        # Generate PDF attachment for Purchase Order
        attachment = frappe.attach_print(
            doctype="Purchase Order",
            name=po.name,
            file_name=f"PurchaseOrder-{po.name}.pdf",
            print_format=None  # use default print format
        )

        # Send the email with attachment
        frappe.sendmail(
            recipients=[recipient_email],
            subject=f"Purchase Receipt {doc.name} for PO {po.name}",
            message=msg,
            attachments=[attachment]
        )
    else:
        # No email for PO owner → warn the user, but do not block submission
        frappe.msgprint(
            msg=_("No email associated with PO owner <b>{0}</b>. "
                  "Purchase Receipt recorded, but PO owner has not been notified."
                  ).format(po.owner),
            title=_("Notification Skipped"),
            indicator="orange"
        )

def set_purchase_order_field(doc, event):
    """
    Ensure the custom_purchase_order field at PR header is filled
    from child items (if not already set).
    """
    if not doc.custom_purchase_order and doc.items:
        first_po = next(
            (i.custom_purchase_order for i in doc.items if i.custom_purchase_order),
            None
        )
        if first_po:
            doc.custom_purchase_order = first_po

def set_reply_to(doc, method):
    user_email = frappe.db.get_value("User", frappe.session.user, "email")
    
    if user_email:
        # Parse existing headers or create new
        headers = {}
        if doc.headers:
            try:
                headers = json.loads(doc.headers)
            except:
                headers = {}
        
        # Add Reply-To header
        headers["Reply-To"] = user_email
        
        # Save back as JSON string
        doc.headers = json.dumps(headers)
