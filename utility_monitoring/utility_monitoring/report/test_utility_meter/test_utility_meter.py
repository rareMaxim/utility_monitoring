# Copyright (c) 2024, Maxim Sysoiev and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import flt
from frappe import _


def execute(filters: dict | None = None):
	"""Return columns and data for the report.

	This is the main entry point for the report. It accepts the filters as a
	dictionary and should return columns and data. It is called by the framework
	every time the report is refreshed or a filter is updated.
	"""
	columns = get_columns()
	data = get_data(filters)

	return columns, data


def get_columns() -> list[dict]:
	return [
		{"fieldname": "address", "label": "Адреса", "fieldtype": "Link", "options": "um Address", "width": 200},
		{"fieldname": "meter_name", "label": "Назва лічильника", "fieldtype": "Link", "options": "um Meter", "width": 200},
		{"fieldname": "service", "label": "Послуга", "fieldtype": "Link", "options": "um Service", "width": 150},
		{"fieldname": "consumption", "label": "Споживання", "fieldtype": "Float", "width": 120},
		{"fieldname": "rate", "label": "Тариф", "fieldtype": "Currency", "width": 120},
		{"fieldname": "total_cost", "label": "Вартість", "fieldtype": "Currency", "width": 120},
	]


def get_data(filters) -> list[list]:
	conditions = []
	if filters.get("address"):
		conditions.append(f"m.address = '{filters['address']}'")
	if filters.get("month"):
		conditions.append(f"MONTH(mr.date) = {filters['month']}")
	if filters.get("year"):
		conditions.append(f"YEAR(mr.date) = {filters['year']}")

	where_clause = " AND ".join(conditions)
	if where_clause:
		where_clause = "WHERE " + where_clause

	query = f"""
		SELECT 
			m.address,
			m.meter_name,
			ms.service_name AS service,
			(mr.current_reading - mr.previous_reading) AS consumption,
			ms.base_rate,
			(ms.base_rate * (mr.current_reading - mr.previous_reading)) AS total_cost
		FROM `tabum Meter Reading` mr
		JOIN `tabum Meter` m ON mr.meter = m.name
		{where_clause}
	"""
	data = frappe.db.sql(query, as_dict=True)

	# Додаємо загальний підсумок
	total_cost = sum(flt(row['total_cost']) for row in data)
	data.append({
		"address": "Загалом",
		"meter_name": "",
		"service": "",
		"consumption": "",
		"rate": "",
		"total_cost": total_cost,
	})

	return data
