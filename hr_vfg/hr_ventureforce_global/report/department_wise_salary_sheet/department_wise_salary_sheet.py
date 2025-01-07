# Copyright (c) 2022, pa and contributors
# For license information, please see license.txt

from functools import total_ordering
import frappe
from frappe import _
from frappe.utils import data, flt

def execute(filters=None):
	columns = get_columns(filters)
	data = get_data(filters)
	return columns, data

def get_columns(filters):
	columns = [
        {
			"label": _("Staff ID"),
			"fieldname": "staff_id",
			"fieldtype": "Data",
			"width": 140,
		},
		{
			"label": _("Name"),
			"fieldname": "employee_name",
			"fieldtype": "Data",
			"width": 220,
		},
		{
			"label": _("Designation"),
			"fieldname": "designation",
			"fieldtype": "Data",
			"width": 140,
		},
		{
			"label": _("Period"),
			"fieldname": "period",
			"fieldtype": "Data",
			"width": 140,
		},
		{
			"label": _("Total Days"),
			"fieldname": "total_days",
			"fieldtype": "Float",
			"width": 140,
		},
		{
			"label": _("Wages Rate"),
			"fieldname": "wages_rate",
			"fieldtype": "Currency",
			"width": 140,
		},
		{
			"label": _("OT Hrs"),
			"fieldname": "ot_hrs",
			"fieldtype": "Float",
			"width": 140,
		},
		{
			"label": _("Double Duty"),
			"fieldname": "extra_duty_full_day",
			"fieldtype": "Float",
			"width": 140,
		},
		{
			"label": _("Monthly Salary/Wages"),
			"fieldname": "basic",
			"fieldtype": "Currency",
			"width": 140,
		},
		{
			"label": _("Payment Mode"),
			"fieldname": "p_mode",
			"fieldtype": "Data",
			"width": 140,
		},
		
		{
			"label": _("Holiday"),
			"fieldname": "no_of_holiday",
			"fieldtype": "Float",
			"width": 140,
		},
		{
			"label": _("Holiday Amnt"),
			"fieldname": "holiday_ot_amount",
			"fieldtype": "Currency",
			"width": 140,
		},
		{
			"label": _("Holiday OT"),
			"fieldname": "holiday_ot",
			"fieldtype": "Float",
			"width": 140,
		},
		{
			"label": _("OT Hours Amnt"),
			"fieldname": "ot_hours_amount",
			"fieldtype": "Currency",
			"width": 140,
		},
		{
			"label": _("D.Duty"),
			"fieldname": "extra_duty",
			"fieldtype": "Currency",
			"width": 140,
		},
		{
			"label": _("Eid Holidays"),
			"fieldname": "eid_holidays",
			"fieldtype": "Currency",
			"width": 140,
		},
		{
			"label": _("Fuel&Mobile"),
			"fieldname": "fuel_mobile_allw",
			"fieldtype": "Currency",
			"width": 140,
		},
		{
			"label": _("Advance"),
			"fieldname": "adv_loan",
			"fieldtype": "Currency",
			"width": 140,
		},
		{
			"label": _("Loan"),
			"fieldname": "loan",
			"fieldtype": "Currency",
			"width": 140,
		},
		{
			"label": _("Reward"),
			"fieldname": "reward",
			"fieldtype": "Currency",
			"width": 140,
		},
		{
			"label": _("House Rent"),
			"fieldname": "house_rent",
			"fieldtype": "Currency",
			"width": 140,
		},
		{
			"label": _("Product in Prize"),
			"fieldname": "p_and_p",
			"fieldtype": "Currency",
			"width": 140,
		},
		{
			"label": _("Gross Pay"),
			"fieldname": "gross_pay",
			"fieldtype": "Currency",
			"width": 140,
		},
		
		{
			"label": _("Arrears"),
			"fieldname": "arrears",
			"fieldtype": "Currency",
			"width": 140,
		},
		{
			"label": _("Lates"),
			"fieldname": "lates_for_absents",
			"fieldtype": "Float",
			"width": 140,
		},
		{
			"label": _("Late Amount"),
			"fieldname": "late_ded",
			"fieldtype": "Currency",
			"width": 140,
		},
		{
			"label": _("Cont."),
			"fieldname": "total_deduction",
			"fieldtype": "Currency",
			"width": 140,
		},
		{
			"label": _("Net Salary"),
			"fieldname": "net_pay",
			"fieldtype": "Currency",
			"width": 140,
		},
		{
			"label": _("Tax"),
			"fieldname": "income_tax",
			"fieldtype": "Currency",
			"width": 140,
		},
		{
			"label": _("Through Cheque"),
			"fieldname": "paid_cheque",
			"fieldtype": "Currency",
			"width": 140,
		},
		{
			"label": _("CASH"),
			"fieldname": "paid_cash",
			"fieldtype": "Currency",
			"width": 140,
		},
		
		
		
	]

	return columns

def get_conditions(filters=None):
	conditions = {
		"month":filters.get("month"),
		"year":filters.get("year"),
	}
	
	if filters.get('department'):
		conditions["department"] = filters.get('department')
	if filters.get('employee'):
		conditions["employee"] = filters.get('employee')
	return conditions

def get_data(filters):
	conditions = get_conditions(filters)
	data =[]

	sql = frappe.db.get_all("Salary Slip",filters=conditions,fields=["name"],order_by="department ASC")
	cur_dpt = None

	total_cash = 0
	total_deduction = 0
	total_gross = 0
	net_pay = 0
	total_cheque = 0
	g_total_gross = 0
	g_total_cheque = 0
	g_total_cash = 0
	g_total_deduction = 0
	g_net_pay = 0
	for l in sql:
		doc = frappe.get_doc("Salary Slip",l.name)
		basic = 0
		arrears = 0
		fuel_mobile = 0
		holiday_ot_amount = 0
		ot_amount = 0
		extra_duty = 0
		p_and_p = 0
		reward = 0
		house_rent = 0
		eid_holidays = 0
		late_ded = 0
		for er in doc.earnings:
			if "basic" in er.salary_component.lower():
				basic = er.amount
			elif "arrears" in er.salary_component.lower():
				arrears = er.amount
			elif "fuel" in er.salary_component.lower() or "mobile" in er.salary_component.lower():
				fuel_mobile = er.amount
			elif "holiday overtime" in er.salary_component.lower():
				holiday_ot_amount = er.amount
			elif "overtime" in er.salary_component.lower():
				ot_amount = er.amount
			elif "extra duty" in er.salary_component.lower():
				extra_duty = er.amount
			elif "product in prize" in er.salary_component.lower():
				p_and_p = er.amount
			elif "reward" in er.salary_component.lower():
				reward = er.amount
			elif "house rent" in er.salary_component.lower():
				house_rent = er.amount
			elif "late deduction" in er.salary_component.lower():
				late_ded = er.amount
			elif "eid holidays" in er.salary_component.lower():
				eid_holidays = er.amount
		income_tax = 0
		for de in doc.deductions:
			if de.salary_component.lower() == "income tax":
				income_tax = de.amount
		adv_loans = 0
		loan = 0
		for l in doc.loans:
			if "advance" in frappe.db.get_value("Loan",l.loan,"loan_type"):
				adv_loans+=l.total_payment
			else:
				loan+=l.total_payment

		
		
		if not cur_dpt:
			cur_dpt = doc.department
			data.append({
				'staff_id':"<b>"+(doc.department or "NA") + "</b>"
			})
			data.append({
				    'staff_id':doc.employee,
					'employee_name':doc.employee_name,
					'designation':doc.designation,
					'total_days': doc.month_days,
					"ot_hours":doc.late_sitting_hours,
					"extra_duty_full_day":doc.holiday_full_day_over_time,
					"basic":basic,
					"p_mode":doc.mode_of_payment,
					"no_of_holiday":doc.total_holidays,
					"holiday_ot_amount":holiday_ot_amount,
					"holiday_ot":doc.holiday_hours,
					"ot_hours_amount":ot_amount,
					"extra_duty":extra_duty,
					"fuel_mobile_allw":fuel_mobile,
					"adv_loan":adv_loans,
					"loan":loan,
					"arrears":arrears,
					'gross_pay':doc.gross_pay,
					'total_deduction':doc.total_deduction,
					'net_pay':doc.net_pay,
					"income_tax":income_tax,
					"paid_cheque":doc.net_pay if doc.mode_of_payment != "Cash" else 0,
					"paid_cash":doc.net_pay if doc.mode_of_payment == "Cash" else 0,
					"lates_for_absents":doc.lates_for_absent,
					"period":str(doc.start_date)+"-"+str(doc.end_date),
					"wages_rate":0,
					"p_and_p" :p_and_p,
					"reward" : reward,
					"house_rent":house_rent,
					"eid_holidays":eid_holidays,
					"late_ded" :late_ded

			})

			if doc.mode_of_payment != "Cash":
				total_cheque+=doc.net_pay
			else:
				total_cash+=doc.net_pay
			total_deduction+=doc.total_deduction
			net_pay += doc.net_pay
			total_gross+=doc.gross_pay
			g_total_gross+=doc.gross_pay
			g_total_cash+=total_cash
			g_total_cheque+=total_cheque
			g_total_deduction += doc.total_deduction
			g_net_pay += doc.net_pay

		elif cur_dpt != doc.department:
			cur_dpt = doc.department
			data.append({
				'staff_id':"<b>SUB TOTAL</b>",
				'total_deduction': total_deduction,
				'net_pay': net_pay,
				"paid_cheque":total_cheque,
				"paid_cash":total_cash,
				"gross_pay":total_gross
			})
			total_cash = 0
			total_deduction = 0
			net_pay = 0
			total_cheque = 0
			total_gross = 0
			data.append({
				'staff_id':"<b>"+(doc.department or "NA" )+ "</b>"
			})
			data.append({
				    'staff_id':doc.employee,
					'employee_name':doc.employee_name,
					'designation':doc.designation,
					'total_days': doc.month_days,
					"ot_hours":doc.late_sitting_hours,
					"extra_duty_full_day":doc.holiday_full_day_over_time,
					"basic":basic,
					"p_mode":doc.mode_of_payment,
					"no_of_holiday":doc.total_holidays,
					"holiday_ot_amount":holiday_ot_amount,
					"holiday_ot":doc.holiday_hours,
					"ot_hours_amount":ot_amount,
					"extra_duty":extra_duty,
					"fuel_mobile_allw":fuel_mobile,
					"adv_loan":adv_loans,
					"loan":loan,
					"arrears":arrears,
					'gross_pay':doc.gross_pay,
					'total_deduction':doc.total_deduction,
					'net_pay':doc.net_pay,
					"income_tax":income_tax,
					"paid_cheque":doc.net_pay if doc.mode_of_payment != "Cash" else 0,
					"paid_cash":doc.net_pay if doc.mode_of_payment == "Cash" else 0,
					"lates_for_absents":doc.lates_for_absent,
					"period":str(doc.start_date)+"-"+str(doc.end_date),
					"wages_rate":0,
					"p_and_p" :p_and_p,
					"reward" : reward,
					"house_rent":house_rent,
					"eid_holidays":eid_holidays,
					"late_ded" :late_ded

			})

			if doc.mode_of_payment != "Cash":
				total_cheque+=doc.net_pay
			else:
				total_cash+=doc.net_pay
			total_deduction+=doc.total_deduction
			net_pay += doc.net_pay
			total_gross+=doc.gross_pay
			g_total_gross+=doc.gross_pay
			g_total_cash+=total_cash
			g_total_cheque+=total_cheque
			g_total_deduction += doc.total_deduction
			g_net_pay += doc.net_pay
		else:
			data.append({
				    'staff_id':doc.employee,
					'employee_name':doc.employee_name,
					'designation':doc.designation,
					'total_days': doc.month_days,
					"ot_hours":doc.late_sitting_hours,
					"extra_duty_full_day":doc.holiday_full_day_over_time,
					"basic":basic,
					"p_mode":doc.mode_of_payment,
					"no_of_holiday":doc.total_holidays,
					"holiday_ot_amount":holiday_ot_amount,
					"holiday_ot":doc.holiday_hours,
					"ot_hours_amount":ot_amount,
					"extra_duty":extra_duty,
					"fuel_mobile_allw":fuel_mobile,
					"adv_loan":adv_loans,
					"loan":loan,
					"arrears":arrears,
					'gross_pay':doc.gross_pay,
					'total_deduction':doc.total_deduction,
					'net_pay':doc.net_pay,
					"income_tax":income_tax,
					"paid_cheque":doc.net_pay if doc.mode_of_payment != "Cash" else 0,
					"paid_cash":doc.net_pay if doc.mode_of_payment == "Cash" else 0,
					"lates_for_absents":doc.lates_for_absent,
					"period":str(doc.start_date)+"-"+str(doc.end_date),
					"wages_rate":0,
					"p_and_p" :p_and_p,
					"reward" : reward,
					"house_rent":house_rent,
					"eid_holidays":eid_holidays,
					"late_ded" :late_ded

			})

			if doc.mode_of_payment != "Cash":
				total_cheque+=doc.net_pay
			else:
				total_cash+=doc.net_pay
			total_deduction+=doc.total_deduction
			net_pay += doc.net_pay
			total_gross+=doc.gross_pay
			g_total_gross+=doc.gross_pay
			g_total_cash+=total_cash
			g_total_cheque+=total_cheque
			g_total_deduction += doc.total_deduction
			g_net_pay += doc.net_pay

	if len(sql) > 0:
		data.append({
					'staff_id':"<b>SUB TOTAL</b>",
				'total_deduction': total_deduction,
				'net_pay': net_pay,
				"paid_cheque":total_cheque,
				"paid_cash":total_cash,
				"gross_pay":total_gross
				})
		data.append({
					'staff_id':"<b>GRAND TOTAL</b>",
					'total_deduction': g_total_deduction,
				'net_pay': g_net_pay,
				"paid_cheque":g_total_cheque,
				"paid_cash":g_total_cash,
				"gross_pay":g_total_gross
				})
	return data


