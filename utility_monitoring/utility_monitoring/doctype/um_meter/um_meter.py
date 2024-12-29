# Copyright (c) 2024, Maxim Sysoiev and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.query_builder import Interval
from frappe.query_builder.functions import Count, CurDate, UnixTimestamp


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

def get_timeline_data(doctype: str, name: str) -> dict[int, int]:
    """get timeline data based on um Meter Reading. This is displayed as heatmap on the item page."""

    sle = frappe.qb.DocType("um Meter Reading")
    result = dict(
        frappe.qb.from_(sle)
        .select(UnixTimestamp(sle.reading_date), Count("*"))
        .where(sle.meter == name)
        .where(sle.reading_date > CurDate() - Interval(years=1))
        .groupby(sle.reading_date)
        .run())
    print(result)
    return result
    
