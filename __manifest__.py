{
    'name': 'Data Import Cleaning',
    'website': 'https://www.odoo.com',
    'author': 'Odoo Inc.',
    'summary': 'Interface for cleaning and formatting uploaded files',
    'description': 'Generate importable csv files from user data',
    'category': 'Custom Development',
    'depends': [ 'base_import', 'web' ],
    'data': [
        'views/cleaner_spec_views.xml',
        'views/data_cleaner_views.xml',
        'security/ir.model.access.csv'
    ],
    'assets': {
        'web.assets_common': [
            'data_cleaner/static/src/css/cleaner_spec.css',
        ],
    },
    'license': 'LGPL-3',
    'website': 'www.odoo.com',
    'application': True,
}