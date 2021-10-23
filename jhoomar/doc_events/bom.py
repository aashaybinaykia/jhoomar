import frappe
from frappe import _

@frappe.whitelist()
def on_sumbit(bom, method):
    if bom.has_variants:
        # Creates BOM for the item variants
        frappe.enqueue(
            create_bom_for_item_variants, bom=bom, queue='short')

        item_variants = frappe.get_list("Item", filters={'variant_of': bom.item})
        frappe.msgprint(_("Item variant BOM creation has been queued for: " + ", ".join([item.name for item in item_variants])))


def create_bom_for_item_variants(bom):
    from erpnext.manufacturing.doctype.bom.bom import make_variant_bom

    bom_no = bom.name
    item_variants = frappe.get_list("Item", filters={'variant_of': bom.item})

    for item_variant in item_variants:
        item_variant_bom = make_variant_bom(
            source_name=bom_no, bom_no=bom_no, item=item_variant.name, variant_items=[])

        item_variant_bom.is_default = bom.is_default
        item_variant_bom.ref_bom = bom_no
        item_variant_bom.save()
        item_variant_bom.submit()


@frappe.whitelist()
def on_cancel(bom, method):
    if bom.has_variants:
        # Cancels BOM for the item variants
        frappe.enqueue(
            cancel_bom_for_item_variants, bom=bom, queue='short')

def cancel_bom_for_item_variants(bom):
    item_variant_boms = frappe.get_list("BOM", filters={'ref_bom': bom.name, 'docstatus': 1})

    for item_variant_bom in item_variant_boms:
        variant_bom = frappe.get_doc("BOM", item_variant_bom.name)
        variant_bom.cancel()


@frappe.whitelist()
def on_update_after_submit(bom, method):
    if bom.has_variants:
        # Updates BOM `is_default` for the item variants
        frappe.enqueue(
            update_bom_default_for_item_variants, bom=bom, queue='short')

def update_bom_default_for_item_variants(bom):
    item_variant_boms = frappe.get_list("BOM", filters={'ref_bom': bom.name, 'docstatus': 1})

    for item_variant_bom in item_variant_boms:
        variant_bom = frappe.get_doc("BOM", item_variant_bom.name)
        variant_bom.is_default = bom.is_default
        variant_bom.save()
        variant_bom.submit()
