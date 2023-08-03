{
    "name": "Data Import Cleaning",
    "website": "https://www.odoo.com",
    "author": "Odoo Inc.",
    "summary": "Interface for cleaning and formatting uploaded files",
    "description": "",
    "category": "Custom Development",
    "depends": [],
    "data": [
        "views/data_cleaner_views.xml",
        "security/data_cleaner_groups.xml",
        "security/ir.model.access.csv"
    ],
    'assets': {
        'web.assets_backend': [
            'static/src/xml/template_bsa_import.xml',
        ],
    },
    "license": "LGPL-3",
    "website": "www.odoo.com",
    "application": True,
}