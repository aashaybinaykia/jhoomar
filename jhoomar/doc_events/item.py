import frappe
from frappe import _

@frappe.whitelist()
def after_insert(item, method):
    if bool(item.variant_of):
        create_item_variant_bom_from_item_template(item)


def create_item_variant_bom_from_item_template(item):
    '''
        :param item: Item Variant 
    '''

    from erpnext.manufacturing.doctype.bom.bom import make_variant_bom

    item_template = item.variant_of

    item_template_bom_list = frappe.get_list("BOM", 
        filters={
            'item': item_template, 
            'docstatus': 1
        }, 
        fields=['name', 'is_default'])

    for item_template_bom in item_template_bom_list:
        bom_no = item_template_bom.name
        item_variant_bom = make_variant_bom(
            source_name=bom_no, bom_no=bom_no, item=item.name, variant_items=[])

        item_variant_bom.is_default = item_template_bom.is_default
        item_variant_bom.ref_bom = bom_no
        item_variant_bom.save()
        item_variant_bom.submit()
