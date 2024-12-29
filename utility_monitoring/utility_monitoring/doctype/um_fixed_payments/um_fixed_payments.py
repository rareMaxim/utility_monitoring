# Copyright (c) 2024, Maxim Sysoiev and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class umFixedPayments(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		address: DF.Link
		amount: DF.Currency
		payment_date: DF.Date | None
		payment_name: DF.Data
		service_provider: DF.Link | None
	# end: auto-generated types

	pass
