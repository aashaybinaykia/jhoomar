
from __future__ import unicode_literals

import frappe
from frappe import _

@frappe.whitelist()
def autoname(pi, method):
    if pi.number:
        autoname_item_code(pi)


def autoname_item_code(pi):
    pi.name = pi.naming_series[:-7] + pi.posting_date[0:4] + "-00" + str(pi.number)
    
