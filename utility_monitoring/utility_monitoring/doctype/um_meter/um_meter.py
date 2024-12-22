# Copyright (c) 2024, Maxim Sysoiev and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class umMeter(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF
		from utility_monitoring.utility_monitoring.doctype.um_meter_services.um_meter_services import umMeterServices

		address: DF.Link | None
		meter_id: DF.Data | None
		meter_name: DF.Data | None
		services: DF.Table[umMeterServices]
	# end: auto-generated types

	pass
