# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from multiprocessing import Condition
import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname
from frappe import msgprint, _
from datetime import datetime
from datetime import timedelta
from datetime import date as dt
import datetime as special
import time
from hrms.hr.utils import get_holidays_for_employee
from frappe.utils import date_diff, add_months, today, getdate, add_days, flt, get_last_day
import calendar

def execute(filters=None):
	columns, data = [], []
	return get_columns(), get_data(filters)

def get_data(filters):
	condition = {
		"month": filters.get("month", None),
		"year": filters.get("year", None)
	}
	if filters.get("depart", None):
		condition["department"] = filters.depart
	if filters.get("employee", None):
		condition["employee"] = filters.employee
	if filters.get("designation", None):
		condition["designation"] = filters.designation
	res = frappe.db.get_all("Employee Attendance", filters=condition, fields=["name"])
	data = []
	# emp_displayed = {}
	for d in res:
		doc = frappe.get_doc("Employee Attendance", d.name)
		employee = doc.employee
		for item in doc.table1:
			# lv = frappe.get_all("Leave Application", filters={"from_date":["<=",getdate(item.date)],"to_date":[">=",getdate(item.date)],"employee":doc.employee,"status":"Approved"},fields=["*"])
			shift_req = frappe.get_all("Shift Request", filters={'employee': doc.employee,
																 'from_date': ["<=", item.date], 'to_date': [">=", item.date]}, fields=["*"])
			shift = None
			if len(shift_req) > 0:
				shift = shift_req[0].shift_type
			else:
				shift_ass = frappe.get_all("Shift Assignment", filters={'employee': doc.employee,
																		'start_date': ["<=", item.date]}, fields=["*"])
				if len(shift_ass) > 0:
					shift = shift_ass[0].shift_type
			if shift == None:
				shift_doc = None

			else:
				shift_doc = frappe.get_doc("Shift Type", shift)

			day_name = datetime.strptime(
				str(item.date), '%Y-%m-%d').strftime('%A')

			day_data = None
			if shift_doc:
				for day in shift_doc.day:
					if day_name == day.day:
						day_data = day
						break
			if not day_data:
				if item.check_in_1 and item.check_out_1:
					schedule_time_in = "00:00:00"
					schedule_time_out = "00:00:00"
				else:
					data.append({
						"day": day_name[:3],
						"day_status": day_name,
						"date": getdate(item.date),
						"att_status": "Weekly Off"
					})
					continue
			else:
				schedule_time_in = day_data.start_time
				schedule_time_out = day_data.end_time
			att_status = "In Time"
			if item.late:
				att_status = "Late Entry"
			elif item.absent:
				att_status = "Absent"
			elif item.half_day:
				att_status = "Half Day"
			if item.weekly_off or item.public_holiday:
				att_status = "Off"
				holidays = get_holidays_for_employee(doc.employee, getdate(
					item.date), getdate(item.date))

				if len(holidays) > 0:
					att_status = holidays[0].description
			if item.type:
				att_status = item.type
			if att_status == "Absent":
				leaves = frappe.get_all("Leave Application", filters={'employee': doc.employee,
																	 'from_date': ["<=", item.date], 'to_date': [">=", item.date], "status": "Approved"}, fields=["*"])
				if len(leaves) > 0:
					att_status = leaves[0].leave_type
			# if employee not in emp_displayed:
			row = {
				"emp_id": doc.employee,
				"name": doc.employee_name,
				"date_of_joining": doc.date_of_joining,
				"relieving_date": doc.relieving_date,
				"department": doc.department,
				"designation": frappe.db.get_value("Employee", {"name": doc.employee}, "designation"),
				"date": getdate(item.date),
				"day": day_name[:3],
				# "schedule_time_in":schedule_time_in,
				"actual_in_time": item.check_in_1,
				"schedule_time_out": schedule_time_out,
				"actual_out_time": item.check_out_1,
				"late_arrival": round(flt((datetime.strptime(str(item.late_coming_hours), "%H:%M:%S").hour * 60) + (datetime.strptime(str(item.late_coming_hours), "%H:%M:%S").minute) + (datetime.strptime(str(item.late_coming_hours), "%H:%M:%S").second / 60)), 2) if item.late and item.late_coming_hours else "00",
				"early_going": round(flt((datetime.strptime(str(item.early_going_hours), "%H:%M:%S").hour * 60) + (datetime.strptime(str(item.early_going_hours), "%H:%M:%S").minute) + (datetime.strptime(str(item.early_going_hours), "%H:%M:%S").second / 60)), 2) if item.early and item.early_going_hours else "00",
				"work_hours": item.per_day_hour,
				"total_hours": item.difference,
				"overtime": item.late_sitting,
				"day_status": "Holiday" if item.weekly_off or item.public_holiday else "Working Day",
				"att_status": att_status
			}
			# 	emp_displayed[employee] = True
			# else:
			# row={
			# 	"emp_id":" ",
			# 	"name":" ",
			# 	"date_of_joining":" ",
			# 	"relieving_date":" ",
			# 	"department":" ",
			# 	"designation":" ",
			# 	"date":getdate(item.date),
			# 	"day":day_name[:3],
			# 	"schedule_time_in":schedule_time_in,
			# 	"actual_in_time":item.check_in_1,
			# 	"schedule_time_out":schedule_time_out,
			# 	"actual_out_time":item.check_out_1,
			# 	"late_arrival":round(flt((datetime.strptime( str(item.late_coming_hours), "%H:%M:%S").hour *60)+(datetime.strptime( str(item.late_coming_hours), "%H:%M:%S").minute)+(datetime.strptime( str(item.late_coming_hours), "%H:%M:%S").second/60)), 2)if item.late and item.late_coming_hours else "00",
			# 	"early_going":round(flt((datetime.strptime( str(item.early_going_hours), "%H:%M:%S").hour *60)+(datetime.strptime( str(item.early_going_hours), "%H:%M:%S").minute)+(datetime.strptime( str(item.early_going_hours), "%H:%M:%S").second/60)), 2)if item.early and item.early_going_hours else "00",
			# 	"work_hours":item.per_day_hour,
			# 	"total_hours":item.difference,
			# 	"overtime":item.late_sitting,
			# 	"day_status":"Holiday" if item.weekly_off or item.public_holiday else "Working Day",
			# 	"att_status":att_status
			# }

			data.append(row)

		if len(doc.table1) > 0:
			data.append({
				"date": "<h4>Summary</h4>"
			})
			data.append({
				"date": "<b>Hours Worked</b>",
				"day": doc.hours_worked,
				"actual_in_time": "<b>Present Days</b>",
				"actual_out_time": doc.present_days,
				"late_arrival": "<b>Total Early Goings</b>",
				"att_status": doc.total_early_goings

			})

			data.append({
				"date": "<b>Late Sitting Hrs</b>",
				"day": doc.late_sitting_hours,
				"actual_in_time": "<b>Total :Lates</b>",
				"actual_out_time": doc.total_lates,
				"late_arrival": "<b>Lates For Absent</b>",
				"att_status": doc.lates_for_absent,


			})

			data.append({
				"date": "<b>Half Days</b>",
				"day": doc.total_half_days,
				"actual_in_time": "<b>Total Absents</b>",
				"actual_out_time": doc.total_absents,
				


			})
			data.append(["<hr>", "<hr>", "<hr>", "<hr>", "<hr>", "<hr>", "<hr>", "<hr>", "<hr>", "<hr>", "<hr>", "<hr>", "<hr>", "<hr>", "<hr>", "<hr>", "<hr>", ])

	return data


def get_columns():
	columns=[
		{
			"label": _("Date"),
			"fieldname": "date",
			"fieldtype": "Data",
			"width": 200
		},
		{
			"label": _("Day"),
			"fieldname": "day",
			"fieldtype": "Data",
			"width": 200
		},
		{
			"label": _("Act In Time"),
			"fieldname": "actual_in_time",
			"fieldtype": "Data",
			"width": 200
		},
		{
			"label": _("Act Out Time"),
			"fieldname": "actual_out_time",
			"fieldtype": "Data",
			"width": 200
		},
		 {
			"label": _("Late Arrival (Min)"),
			"fieldname": "late_arrival",
			"fieldtype": "Data",
			"width": 200
		},
		{
			"label": _("Att Status"),
			"fieldname": "att_status",
			"fieldtype": "Data",
			"width": 120
		},
		{
		 	"label": _("Designation"),
		 	"fieldname": "designation",
		 	"fieldtype": "Data",
		 	"width": 200
		 },
		# {
		# 	"label": _("EMP #"),
		# 	"fieldname": "emp_id",
		# 	"fieldtype": "Link",
		# 	"options": "Employee",
		# 	"width": 120
		# },
		# {
		# 	"label": _("Name"),
		# 	"fieldname": "name",
		# 	"fieldtype": "Data",
		# 	"width": 220
		# },
		# 
		# {
		# 	"label": _("Department"),
		# 	"fieldname": "department",
		# 	"fieldtype": "Data",
		# 	"width": 200
		# },
		# {
		# 	"label": _("Relieving Date"),
		# 	"fieldname": "relieving_date",
		# 	"fieldtype": "Date",
		# 	"width": 120
		# },
		# {
		# 	"label": _("Date of Joining"),
		# 	"fieldname": "date_of_joining",
		# 	"fieldtype": "Date",
		# 	"width": 120
		# },
				
		
		# {
		# 	"label": _("Sch In Time"),
		# 	"fieldname": "schedule_time_in",
		# 	"fieldtype": "Data",
		# 	"width": 120
		# },
		

		# {
		# 	"label": _("Sch Out Time"),
		# 	"fieldname": "schedule_time_out",
		# 	"fieldtype": "Data",
		# 	"width": 120
		# },
		
		#
		# {
		# 	"label": _("Day Status"),
		# 	"fieldname": "day_status",
		# 	"fieldtype": "Data",
		# 	"width": 120
		# },
		

		# {
		# 	"label": _("Work Hours"),
		# 	"fieldname": "work_hours",
		# 	"fieldtype": "Data",
		# 	"width": 120
		# },
		# {
		# 	"label": _("Total Hours"),
		# 	"fieldname": "total_hours",
		# 	"fieldtype": "Data",
		# 	"width": 120
		# },
		# {
		# 	"label": _("Overtime"),
		# 	"fieldname": "overtime",
		# 	"fieldtype": "Data",
		# 	"width": 120
		# },
		# {
		# 	"label": _("Leave Early (Min)"),
		# 	"fieldname": "early_going",
		# 	"fieldtype": "Data",
		# 	"width": 120
		# },

	]
	return columns