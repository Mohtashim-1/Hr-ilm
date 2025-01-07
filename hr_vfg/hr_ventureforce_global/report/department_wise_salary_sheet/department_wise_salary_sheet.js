// Copyright (c) 2023, VFG and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Department Wise Salary Sheet"] = {
	"filters": [
		{
			fieldname:"department",
			label: __("Department"),
			fieldtype: "Link",
			options: "Department",
			//default: 'Office Staff - F'
		},
		{
			"fieldname":"employee",
			"label": __("Employee"),
			"fieldtype": "Link",
			"options": "Employee",
			"reqd": 0,
		
				"get_query": function() {
					var dep = frappe.query_report.get_filter_value('department');
					if(!dep){
						return {
							"doctype": "Employee",
							"filters": {
								
							}
						}
					}
					return {
						"doctype": "Employee",
						"filters": {
							"department": dep,
						}
					}
				}
		},
		{
			"fieldname":"month",
			"label": __("Month"),
			"fieldtype": "Select",
			"options":"\nJanuary\nFebruary\nMarch\nApril\nMay\nJune\nJuly\nAugust\nSeptember\nOctober\nNovember\nDecember",
			"reqd": 1
		},
		{
			"fieldname":"year",
			"label": __("Year"),
			"fieldtype": "Select",
			"options":"\n2022\n2023\n2024\n2025\n2026\n2027\n2028\n2029\n2030",
			"reqd": 1
		}
	]
};
