import frappe
# from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


ADDRESS_CUSTOM_FIELDS = {
    "Address": [
        {
            "fieldname": "custom_zatca",
            "fieldtype": "Section Break",
            "label": "ZATCA",
            "insert_after": "links",
            "collapsible": 1,
            "collapsible_depends_on": "",
        },
        {
            "fieldname": "fetch_from_above",
            "fieldtype": "Check",
            "label": "Fetch From Above",
            "insert_after": "custom_zatca",
            "default": "1",
            "description": "If checked, below fields will Read Only."
        },
        {
            "fieldname": "custom_zatca_address_line_1",
            "fieldtype": "Data",
            "label": "Zatca Address Line 1",
            "insert_after": "fetch_from_above",
        },
        {
            "fieldname": "custom_zatca_address_line_2",
            "fieldtype": "Data",
            "label": "Zatca Address Line 2",
            "insert_after": "custom_zatca_address_line_1",
        },
        {
            "fieldname": "custom_zatca_city",
            "fieldtype": "Data",
            "label": "Zatca City",
            "insert_after": "custom_zatca_address_line_2",
        },
        {
            "fieldname": "custom_zatca_pincode",
            "fieldtype": "Data",
            "label": "Zatca Pincode",
            "insert_after": "custom_zatca_city",
        },
        {
            "fieldname": "custom_zatca_state",
            "fieldtype": "Data",
            "label": "Zatca State",
            "insert_after": "custom_zatca_pincode",
        },
    ],
}







# def set_address_fields():
#     try:
#         fields = {
#             "address_line1": "custom_zatca_address_line_1",
#             "address_line2": "custom_zatca_address_line_2",
#             "city": "custom_zatca_city",
#             "pincode": "custom_zatca_pincode",
#             "state": "custom_zatca_state"
#         }

#         for source, target in fields.items():
#             if frappe.db.has_column("Address", source) and frappe.db.has_column("Address", target):
#                 frappe.db.sql(f"""
#                     UPDATE `tabAddress`
#                     SET `{target}` = `{source}`
#                     WHERE `{source}` IS NOT NULL
#                 """)

#     except Exception:
#         frappe.log_error(frappe.get_traceback(), "ZATCA Address Patch Error")




# def after_install():
#     create_custom_fields(ADDRESS_CUSTOM_FIELDS, ignore_validate=True)
#     set_address_fields()






def before_uninstall():
	delete_custom_fields(ADDRESS_CUSTOM_FIELDS)


def delete_custom_fields(custom_fields):
    """
    :param custom_fields: a dict like `{'Customer': [{'fieldname': 'test', ...}]}`
    """

    for doctypes, fields in custom_fields.items():
        if isinstance(fields, dict):
            # only one field
            fields = [fields]

        if isinstance(doctypes, str):
            # only one doctype
            doctypes = (doctypes,)

        for doctype in doctypes:
            fieldnames_to_delete = []

            for field in fields:
                fieldname = field.get("fieldname")
                if not fieldname:
                    continue

                exists = frappe.db.exists("Custom Field", {"fieldname": fieldname, "dt": doctype})
                if exists:
                    fieldnames_to_delete.append(fieldname)

            if fieldnames_to_delete:
                frappe.db.delete(
                    "Custom Field",
                    {
                        "fieldname": ("in", fieldnames_to_delete),
                        "dt": doctype,
                    },
                )
                frappe.clear_cache(doctype=doctype)


