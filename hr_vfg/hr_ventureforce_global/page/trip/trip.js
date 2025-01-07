frappe.pages['trip'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Trip',
		single_column: true
	});
}