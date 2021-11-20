
from __future__ import unicode_literals

import frappe
from frappe import _


@frappe.whitelist()
def make_debit_note(source_name, target_doc=None):
	from jhoomar.controllers.sales_and_purchase_return import make_return_doc
	return make_return_doc("Purchase Invoice", source_name, target_doc)
