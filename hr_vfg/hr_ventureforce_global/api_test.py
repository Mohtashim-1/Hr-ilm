import frappe

@frappe.whitelist(allow_guest=True)
def login():
    frappe.local.form_dict['cmd'] = 'login'
    frappe.conf.allow_cors = True
    frappe.local.cookie_manager.set_cookie("SameSite",None)
    frappe.local.cookie_manager.set_cookie("Secure",0)
    return 1/0
    frappe.local.http_request = frappe.auth.HTTPRequest()
    

    