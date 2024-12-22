# Copyright (c) 2024, Maxim Sysoiev and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class umMeterReading(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF
        from utility_monitoring.utility_monitoring.doctype.um_meter_readin_service_breakdown.um_meter_readin_service_breakdown import umMeterReadinservice_breakdown

        consumption: DF.Float
        current_reading: DF.Float
        meter: DF.Link | None
        previous_reading: DF.Float
        reading_date: DF.Datetime | None
        service_breakdown: DF.Table[umMeterReadinservice_breakdown]
        total_amount: DF.Currency
    # end: auto-generated types

    def before_save(self):
        if self.current_reading and self.previous_reading:
            # Розрахунок споживання
            self.consumption = self.current_reading - self.previous_reading
            total = 0

            # Розрахунок витрат для кожної послуги
            for service in self.service_breakdown:
                service_details = frappe.get_doc(
                    "um Service", service.service_name)
                service.rate = service_details.base_rate + \
                    (service_details.additional_rate or 0)
                service.consumption = self.consumption
                service.amount = service.consumption * service.rate
                total += service.amount

            # Оновлення загальної суми
            self.total_amount = total
