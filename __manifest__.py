{
    "name": "Data Import Cleaning",
    "website": "https://www.odoo.com",
    "author": "Odoo Inc.",
    "summary": "Interface for cleaning and formatting uploaded files",
    "description": "Generate importable csv files from user data",
    "category": "Custom Development",
    "depends": [ "base_import" ],
    "data": [
        "views/data_cleaner_views.xml",
        "security/data_cleaner_groups.xml",
        "security/ir.model.access.csv"
    ],
    "license": "LGPL-3",
    "website": "www.odoo.com",
    "application": True,
}