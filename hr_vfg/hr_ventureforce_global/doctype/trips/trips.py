# -*- coding: utf-8 -*-
# Copyright (c) 2019, Frappe Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from datetime import datetime
from frappe.utils import cint, cstr, date_diff, add_months,flt,add_days ,formatdate,today, getdate, get_link_to_form, \
	comma_or, get_fullname
class Trips(Document):
	def on_trash(self):
		frappe.db.sql(''' DELETE from `tabLocation History` where trip_name=%s''',(self.name))
		frappe.db.commit()

@frappe.whitelist()
def update_user_data(form,lat,long):
	timestamp= datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	doc = frappe.new_doc('Location History')
	doc.trip_name=form
	doc.user_name = frappe.session.user
	doc.lat = lat
	doc.long=long
	doc.datetime=timestamp
	doc.date=today()
	doc.insert(ignore_permissions=True)
	frappe.db.commit()
	return frappe.get_all("Location History",filters={'user_name':frappe.session.user,'trip_name':form},fields=['*'],order_by='creation ASC')

@frappe.whitelist()
def get_user_data(form):
	return frappe.get_all("Location History",filters={'trip_name':form},fields=['*'],order_by='creation ASC')

@frappe.whitelist()
def log_error(messageOrEvent, source, lineno,error,file):
    frappe.log_error(file+","+messageOrEvent+", "+source+", "+str(lineno)+", "+error, 'Front End')


@frappe.whitelist()
def create_logs(check_type,date,user_id,name):
	biometric_id= frappe.db.get_value("Employee",{"user_id":user_id},"biometric_id")
	if not biometric_id:
		frappe.throw("Please make sure that currently loged in user is tagged with some employee.")
		
	if check_type == 'Check In':
			exists = frappe.db.get_value("Attendance Logs",
								{"attendance_date":date,"type":check_type,"biometric_id":biometric_id},"name") or None
			if exists:
				return True
				
		
	doc1 = frappe.new_doc("Attendance Logs")
	doc1.biometric_id = biometric_id
	doc1.attendance = "&lt;Attendance&gt;: "+doc1.biometric_id+" : "+str(date)+" "+str(frappe.utils.get_datetime()).split(" ")[1]+" (1, 1)"
	doc1.attendance_date= date
	doc1.ip = "Trip:"+str(name or "")
	doc1.attendance_time= str(frappe.utils.get_datetime()).split(" ")[1]
	doc1.type = check_type
	doc1.save(ignore_permissions=True)
	doc1.get_employee_attendance(force_update=True,att_type="Trip")

	return True