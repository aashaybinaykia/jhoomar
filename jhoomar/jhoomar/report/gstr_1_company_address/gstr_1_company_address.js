// Copyright (c) 2016, Jhoomar and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["GSTR-1 Company Address"] = {
	"filters": [
		{
			"fieldname": "company_address",
			"label": __("Address"),
			"fieldtype": "Link",
			"options": "Address",
			"reqd": 1,
			"get_query": function () {
				return {
					filters: {
						'is_your_company_address': true,
					}
				}
			}
		},
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"reqd": 1,
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -3),
			"width": "80"
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"reqd": 1,
			"default": frappe.datetime.get_today()
		},
		{
			"fieldname": "type_of_business",
			"label": __("Type of Business"),
			"fieldtype": "Select",
			"reqd": 1,
			"options": ["B2B", "B2C Large", "B2C Small", "CDNR", "EXPORT"],
			"default": "B2B"
		}
	],
	onload: function (report) {

		report.page.add_inner_button(__("Download as JSON"), function () {
			var filters = report.get_values();

			frappe.call({
				method: 'jhoomar.jhoomar.report.gstr_1_company_address.gstr_1_company_address.get_json',
				args: {
					data: report.data,
					report_name: report.report_name,
					filters: filters
				},
				callback: function(r) {
					if (r.message) {
						const args = {
							cmd: 'jhoomar.jhoomar.report.gstr_1_company_address.gstr_1_company_address.download_json_file',
							data: r.message.data,
							report_name: r.message.report_name,
							report_type: r.message.report_type
						};
						open_url_post(frappe.request.url, args);
					}
				}
			});
		});
	}
};
