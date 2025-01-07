# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt
from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class SalaryTransfer(Document):
	pass
	def validate(self):
		if self.transfer_type == "Salary Transfer" and self.mode_of_payment == "Bank":
			get_employees(self)
		if self.transfer_type == "Daily Allowance Transfer" and self.mode_of_payment == "Bank":
			get_allowance_employees(self)
		if self.transfer_type == "Salary Transfer" and self.mode_of_payment == "Cheque":
			get_cheque_employees(self)
		if self.transfer_type == "Daily Allowance Transfer" and self.mode_of_payment == "Cheque":
			get_allowance_cheque_employees(self)

	def before_update_after_submit(self):
		total(self)

	def on_submit(self):
		if self.mode_of_payment != "Cheque":
			create_jv(self)
		if self.mode_of_payment == "Cheque":
			create_cheque_jv(self)



def get_employees(self):
	self.salary_transfer_employees.clear()
	emprec = frappe.db.sql("select name from `tabEmployee` where status = 'Active' and salary_mode = 'Bank' and bank_name = %s", self.bank_account)
	for er in emprec:
		sals = frappe.db.sql("select max(name) from `tabSalary Slip` where employee = %s and month = %s and year =%s and status = 'Submitted'", (er[0], self.select_month, self.year))
		for ss in sals:
			employees = frappe.get_all("Salary Slip", filters={"name": ss[0]}, fields=["employee", "net_pay", "name", "employee_name"])
			for sal in employees:
				amount = int(employees[0]['net_pay'])
				acc = frappe.get_value('Employee', employees[0]['employee'], 'bank_ac_no')
				biometric_id = frappe.get_value('Employee', employees[0]['employee'], 'biometric_id')
				employee_name = frappe.get_value('Employee', employees[0]['employee'], 'first_name')
				cnic = frappe.get_value('Employee', employees[0]['employee'], 'cnic')
				branches_name = frappe.get_value('Employee', employees[0]['employee'], 'branch')
				self.append('salary_transfer_employees', {'employee_id': employees[0]['employee'],'employee_code': biometric_id,'employee_name': employee_name,'cnic': cnic,'account_no': acc,'branches_name':branches_name,'amount': amount})
				#self.save()
				total(self)
def get_cheque_employees(self):
	self.salary_transfer_employees.clear()
	if not self.cheque_transfer_employees:
		emprec = frappe.db.sql("select name from `tabEmployee` where status = 'Active' and salary_mode = 'Cheque'")
		for er in emprec:
			sals = frappe.db.sql("select max(name) from `tabSalary Slip` where employee = %s and month = %s and year =%s and status = 'Submitted'", (er[0], self.select_month, self.year))
			for ss in sals:
				employees = frappe.get_all("Salary Slip", filters={"name": ss[0]}, fields=["employee", "net_pay", "name", "employee_name"])
				for sal in employees:
					amount = int(employees[0]['net_pay'])
					acc = frappe.get_value('Employee', employees[0]['employee'], 'bank_ac_no')
					biometric_id = frappe.get_value('Employee', employees[0]['employee'], 'biometric_id')
					employee_name = frappe.get_value('Employee', employees[0]['employee'], 'first_name')
					cnic = frappe.get_value('Employee', employees[0]['employee'], 'cnic')
					branches_name = frappe.get_value('Employee', employees[0]['employee'], 'branch')
					self.append('cheque_transfer_employees', {'employee_id': employees[0]['employee'],'employee_code': biometric_id,'employee_name': employee_name,'cnic': cnic,'account_no': acc,'branches_name': branches_name,'amount': amount})
					#self.save()
					cheque_total(self)

def get_allowance_employees(self):
	self.salary_transfer_employees.clear()
	emprec = frappe.db.sql("select name from `tabEmployee` where status = 'Active' and salary_mode = 'Bank' and bank_name = %s", self.bank)
	for er in emprec:
		sals = frappe.db.sql("select max(name) from `tabDaily Refresher Allowance` where employee = %s and select_month = %s and year =%s and docstatus = 1", (er[0], self.select_month, self.year))
		for ss in sals:
			employees = frappe.get_all("Daily Refresher Allowance", filters={"name": ss[0]}, fields=["employee", "balance_amount", "name", "employee_name"])
			for sal in employees:
				amount = int(employees[0]['balance_amount'])
				acc = frappe.get_value('Employee', employees[0]['employee'], 'bank_ac_no')
				biometric_id = frappe.get_value('Employee', employees[0]['employee'], 'biometric_id')
				file_number = frappe.get_value('Employee', employees[0]['employee'], 'file_number')
				employee_name = frappe.get_value('Employee', employees[0]['employee'], 'first_name')
				cnic = frappe.get_value('Employee', employees[0]['employee'], 'cnic')
				branch_code = frappe.get_value('Employee', employees[0]['employee'], 'branch_code')
				branches_name = frappe.get_value('Employee', employees[0]['employee'], 'branches_name')
				self.append('salary_transfer_employees', {'employee_id': employees[0]['employee'],'employee_code': biometric_id,'employee_file_no': file_number,'employee_name': employee_name,'cnic': cnic,'branch_code': branch_code,'account_no': acc,'branches_name': branches_name,'amount': amount})
				#self.save()
				total(self)
def get_allowance_cheque_employees(self):
	self.salary_transfer_employees.clear()
	emprec = frappe.db.sql("select name from `tabEmployee` where status = 'Active' and salary_mode = 'Cheque'")
	for er in emprec:
		sals = frappe.db.sql("select max(name) from `tabDaily Refresher Allowance` where employee = %s and select_month = %s and year =%s and docstatus = 1", (er[0], self.select_month, self.year))
		for ss in sals:
			employees = frappe.get_all("Daily Refresher Allowance", filters={"name": ss[0]}, fields=["employee", "balance_amount", "name", "employee_name"])
			for sal in employees:
				amount = int(employees[0]['balance_amount'])
				acc = frappe.get_value('Employee', employees[0]['employee'], 'bank_ac_no')
				biometric_id = frappe.get_value('Employee', employees[0]['employee'], 'biometric_id')
				file_number = frappe.get_value('Employee', employees[0]['employee'], 'file_number')
				employee_name = frappe.get_value('Employee', employees[0]['employee'], 'first_name')
				cnic = frappe.get_value('Employee', employees[0]['employee'], 'cnic')
				branch_code = frappe.get_value('Employee', employees[0]['employee'], 'branch_code')
				branches_name = frappe.get_value('Employee', employees[0]['employee'], 'branches_name')
				self.append('salary_transfer_employees', {'employee_id': employees[0]['employee'],'employee_code': biometric_id,'employee_file_no': file_number,'employee_name': employee_name,'cnic': cnic,'branch_code': branch_code,'account_no': acc,'branches_name': branches_name,'amount': amount})
				#self.save()
				total(self)
def total(self):
	total = 0
	for row in self.salary_transfer_employees:
		total += row.amount
	self.total = total
def cheque_total(self):
	total = 0
	for row in self.cheque_transfer_employees:
		total += row.amount
	self.total = total


def create_jv(self):
	doc = frappe.new_doc("Journal Entry")
	doc.posting_date = self.posting_date
	doc.naming_series = "JV.-"
	doc.voucher_type = "Journal Entry"

	total_credit_amount = 0

	for child in self.salary_transfer_employees:
		if child.amount > 0:
			row = doc.append('accounts')
			row.account = "Payroll Payable - TIF"
			row.party_type = "Employee"
			row.party = child.employee_id
			row.debit_in_account_currency = child.amount

			total_credit_amount += child.amount

	credit_row = doc.append('accounts')
	credit_row.account = frappe.db.get_value("Bank Account", self.bank_account, 'account')
	credit_row.credit_in_account_currency = self.total
	doc.cheque_no = self.cheque_no
	doc.cheque_date = self.cheque_date
	doc.user_remark = self.user_remark
	doc.save()
	doc.submit()
def create_cheque_jv(self):
	doc = frappe.new_doc("Journal Entry")
	doc.posting_date = self.posting_date
	doc.naming_series = "JV.-"
	doc.voucher_type = "Journal Entry"

	total_credit_amount = 0

	for child in self.cheque_transfer_employees:
		if child.amount > 0:
			row = doc.append('accounts')
			row.account = "Payroll Payable - TIF"
			row.party_type = "Employee"
			row.party = child.employee_id
			row.debit_in_account_currency = child.amount
			row.cheque_no = child.cheque

			total_credit_amount += child.amount

	credit_row = doc.append('accounts')
	credit_row.account = frappe.db.get_value("Bank Account", self.bank_account, 'account')
	credit_row.credit_in_account_currency = self.total
	doc.cheque_no = self.cheque_no
	doc.cheque_date = self.cheque_date
	doc.user_remark = self.user_remark
	doc.save()
	doc.submit()
