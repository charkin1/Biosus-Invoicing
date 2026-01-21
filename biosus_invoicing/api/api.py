import frappe
from frappe import _
from frappe.utils import get_url_to_form, strip_html, escape_html


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

    # Build an aggregation of PR quantities keyed by PO rowname (purchase_order_item)
    # This avoids collisions when item_code is the same for multiple rows.
    pr_by_po_row = {}
    for it in doc.items:
        key = it.purchase_order_item
        if not key:
            continue
        data = pr_by_po_row.setdefault(key, {"qty": 0.0, "rejected_qty": 0.0})
        data["qty"] += it.qty or 0
        data["rejected_qty"] += it.rejected_qty or 0

    # Fallback map by item_code only for PO items that do not have a linked PR row.
    pr_by_item_code = {}
    for it in doc.items:
        if it.item_code:
            data = pr_by_item_code.setdefault(it.item_code, {"qty": 0.0, "rejected_qty": 0.0})
            data["qty"] += it.qty or 0
            data["rejected_qty"] += it.rejected_qty or 0

    def po_label(po_item):
        """Build a readable label from PO item."""
        desc = (po_item.description or "").strip()
        desc = strip_html(desc) if desc else ""
        return desc or po_item.item_name or po_item.item_code or "Item"

    def pr_label(pr_item):
        """Build a readable label from PR item."""
        desc = (pr_item.description or "").strip()
        desc = strip_html(desc) if desc else ""
        return desc or pr_item.item_name or pr_item.item_code or "Item"

    # 1) Damaged items list (use each PR row so user sees exactly what was rejected)
    for pr_item in doc.items:
        if pr_item.rejected_qty and pr_item.rejected_qty > 0:
            issues.append(f"{pr_label(pr_item)}: {pr_item.rejected_qty} rejected (damaged)")

    # 2) Missing / partial items per PO row
    for po_item in po.items:
        # Try exact match by PO child rowname first
        agg = pr_by_po_row.get(po_item.name)

        # If no direct link found, try fallback by item_code
        if not agg and po_item.item_code:
            agg = pr_by_item_code.get(po_item.item_code)

        received = 0.0
        if agg:
            received = (agg.get("qty") or 0) + (agg.get("rejected_qty") or 0)

        if received <= 0:
            issues.append(
                f"{po_label(po_item)}: missing completely (ordered {po_item.qty})"
            )
        elif received < (po_item.qty or 0):
            missing = (po_item.qty or 0) - received
            issues.append(
                f"{po_label(po_item)}: {missing} missing "
                f"(ordered {po_item.qty}, received {received})"
            )

    # 3) Build email message body
    if issues:
        issues_html = "".join([f"<li>{escape_html(i)}</li>" for i in issues])
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

    # 4) Handle recipient email (PO creator/owner)
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
            msg=_(
                "No email associated with PO owner <b>{0}</b>. "
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