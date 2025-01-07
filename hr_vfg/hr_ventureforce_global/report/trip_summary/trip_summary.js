// Copyright (c) 2024, VFG and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Trip Summary"] = {
	"filters": [
		{
			fieldname:"from_date",
			label: __("From"),
			fieldtype: "Date",
			reqd:1,
			default: frappe.datetime.month_start(),//frappe.datetime.get_today(),
		},
		{
			fieldname:"to_date",
			label: __("To"),
			fieldtype: "Date",
			reqd:1,
			default: frappe.datetime.get_today(),
		},
		{
			fieldname:"user_id",
			label: __("User"),
			fieldtype: "Link",
			options: "User",
		},
		{
			fieldname:"project",
			label: __("Location"),
			fieldtype: "Link",
			options: "Project",
		},
	]
};
