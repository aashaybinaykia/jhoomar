
from __future__ import unicode_literals

import frappe
from frappe import _


@frappe.whitelist()
def autoname(doc, method):
    if doc.number or doc.number > 0:
        doc.name = doc.naming_series[0:5] + "23-00" + str(doc.number)
