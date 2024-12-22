# Copyright (c) 2024, Maxim Sysoiev and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class umMeterReadinservice_breakdown(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		amount: DF.Currency
		consumption: DF.Float
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		rate: DF.Currency
		service_name: DF.Link | None
	# end: auto-generated types

	pass
