# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname
from frappe import msgprint, _
from datetime import datetime
from datetime import timedelta
from datetime import date as dt
import datetime as special
import time
import json

from frappe.utils import date_diff, add_months, today, getdate, add_days, flt, get_last_day
import calendar

def execute(filters=None):
	columns, data = [], []
	return get_columns(), get_data(filters)

def get_data(filters):
		cond={"date" : ["between",[filters.from_date,filters.to_date]] }
		if filters.get("project"):
			cond["project"] = filters.get("project")
		if filters.get("user_id"):
			cond["user_detail"] = filters.get("user_id")
		result = frappe.db.get_all("Trips",filters=cond,fields=["*"])
		data =[]
		if result:
			for res in result:
				location = ""
				v_type  = ""
				distance = 0
				time_s = ""
				if res.check_in == 1:
					location = res.check_in_location
					v_type = "Check In"
					distance = res.check_in_distance
					time_s = res.check_in_time
				elif res.check_out == 1:
					location = res.check_out_location
					v_type = "Check Out"
					distance = res.check_out_distance
					time_s = res.check_ou_time
				elif res.office_visti:
					location = res.office_location
					v_type = "Office Visit In"
					distance = res.office_distance
					time_s = res.visit_time
				elif res.client_visit_out:
					location = res.office_location
					v_type = "Office Visit Out"
					distance = res.office_distance
					time_s = res.visit_time
				row = {
					"date":res.date,
					"user_id":res.user_detail,
					"visit_place":res.project,
					"location":location,
					"v_type":v_type,
					"distance":distance,
					"time":time_s,
					"remarks":res.remarks
				}
				data.append(row)
		return data

def get_columns():
	columns=[
		{
			"label": _("Date"),
			"fieldname": "date",
			"fieldtype": "Date",
			"width": 220
		},
		{
			"label": _("User Name"),
			"fieldname": "user_id",
			"fieldtype": "Link",
			"options": "User",
			"width": 120
		},
		{
			"label": _("Visit Place"),
			"fieldname": "visit_place",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label": _("Location"),
			"fieldname": "location",
			"fieldtype": "Data",
			"width": 220
		},
		{
			"label": _("Type"),
			"fieldname": "v_type",
			"fieldtype": "Data",
			"width": 200
		},
		{
			"label": _("KM"),
			"fieldname": "distance",
			"fieldtype": "Float",
			"width": 120
		},
		{
			"label": _("Time"),
			"fieldname": "time",
			"fieldtype": "Data",
			"width": 120
		},
		
		{
			"label": _("Remarks"),
			"fieldname": "remarks",
			"fieldtype": "Data",
			"width": 220
		},
		
	]
	return columns