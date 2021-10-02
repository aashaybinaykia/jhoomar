// Copyright (c) 2016, Jhoomar and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Jhoomar Item Variant Details"] = {
	"filters": [
		{
			reqd: 1,
			default: "",
			options: "Item",
			label: __("Item"),
			fieldname: "item",
			fieldtype: "Link",
			get_query: () => {
				return {
					filters: { "has_variants": 1 }
				}
			}
		}
	]
};
