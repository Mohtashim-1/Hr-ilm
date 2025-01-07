frappe.query_reports["Monthly Individual Attendence"] = {
	"filters": [
		{
			fieldname:"employee2",
			label: __("Employee"),
			fieldtype: "Data",
 
 
		},
		{
			fieldname:"depart",
			label: __("Department"),
			fieldtype: "Link",
			options: "Department",
			//default: 'Office Staff - F'
		},
		{
			fieldname:"designation",
			label: __("Designation"),
			fieldtype: "Link",
			options: "Designation",
 
		},
 

		{
			"fieldname":"employee",
			"label": __("Employee"),
			"fieldtype": "Link",
			"options": "Employee",
			"reqd": 0,
 
				"get_query": function() {
					var dep = frappe.query_report.get_filter_value('depart');
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
			"options":"\n2023\n2024\n2025",
			"reqd": 1
		},

	]
};