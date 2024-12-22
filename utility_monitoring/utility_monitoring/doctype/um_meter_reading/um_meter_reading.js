// Copyright (c) 2024, Maxim Sysoiev and contributors
// For license information, please see license.txt

function updateTableServiceBrake(frm) {
    // Отримуємо всі послуги, прив'язані до вибраного лічильника
    frappe.call({
        method: "frappe.client.get",
        args: {
            doctype: "um Meter",
            name: frm.doc.meter
        },
        callback: function (r) {
            if (r.message) {
                // Очищаємо таблицю, щоб підвантажити нові послуги
                frm.clear_table("service_breakdown");

                // Додаємо послуги до таблиці service_breakdown
                r.message.services.forEach(function (service) {
                    frm.add_child("service_breakdown", {
                        service_name: service.service,
                        service_rate: service.service_rate
                    });
                });

                frm.refresh_field("service_breakdown");
            }
        }
    });
}

function fillPrevouseData(frm) {

    frappe.call({
        method: "frappe.client.get_list",
        args: {
            doctype: "um Meter Reading",
            filters: {
                meter: frm.doc.meter
            },
            fields: ["current_reading", "reading_date"],
            order_by: "reading_date desc",
            limit_page_length: 1
        },
        callback: function (r) {
            if (r.message && r.message.length > 0) {
                // Заповнюємо попередні показники
                frm.set_value("previous_reading", r.message[0].current_reading);
                frm.refresh_field("previous_reading");
            } else {
                // Якщо немає попередніх даних
                frm.set_value("previous_reading", 0);
                frm.refresh_field("previous_reading");
            }
        }
    });
}

frappe.ui.form.on("um Meter Reading", {
    refresh(frm) {

    },
    current_reading: function (frm) {
        if (frm.doc.current_reading && frm.doc.previous_reading) {
            frm.doc.consumption = frm.doc.current_reading - frm.doc.previous_reading;
            frm.doc.total_amount = frm.doc.consumption * frm.doc.meter_type_rate;
            frm.refresh_fields(['consumption', 'total_amount']);
        }
    },
    meter: function (frm) {
        if (frm.doc.meter) {
            updateTableServiceBrake(frm);
            fillPrevouseData(frm);
        }
    }
});
