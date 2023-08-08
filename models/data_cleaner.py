from odoo import api, fields, models
from io import StringIO
from base64 import b64decode, b64encode

class DataCleaner(models.Model):
    _name = 'data.cleaner'
    _description = 'Tool for importing and cleaning client data'
    
    file_loaded = fields.Boolean(string="Is File Loaded", default=False)
    file = fields.Binary(string="Uploaded File")
    csv_data = fields.Char(string="Unformatted CSV Data")
    cleaned_csv = fields.Char(default='Test')
    exportable_csv = fields.Binary()
    
    specs = fields.One2many(comodel_name='cleaner.spec', inverse_name='parent', string='Data Specifications')

    # Update loaded status for field visibility
    @api.onchange('file')
    def _onchange_file(self):
        self.file_loaded = True if self.file else False

    # Load data and build wizard
    def open_wizard(self):
        self.ensure_one
        data = self.decode_file()
        spec = self.env['cleaner.spec'].create({})
        spec.parent = self.id
        spec.process_data(data)
        return {
            'name': 'data.mapping.wizard',
            'type': 'ir.actions.act_window',
            'res_model': 'cleaner.spec',
            'view_mode': 'form',
            'view_id': self.env.ref('data_cleaner.view_cleaner_spec_form').id,
            'target': 'new',
        }

    # Decode file data for processing
    def decode_file(self) -> StringIO:
        return StringIO(b64decode(self.file).decode('utf-8'))

    # Export the formatted file and set variables back to default
    def export_csv(self):
        res = self.download_cleaned_csv()
        self.file_loaded = 'not_loaded'
        self.file = None
        return res

    # Generate the CSV file from the cleaned data and execute download
    def download_cleaned_csv(self):
        self.exportable_csv = b64encode(bytes(self.cleaned_csv, encoding='utf8'))
        return {
            'name': 'FEC',
            'type': 'ir.actions.act_url',
            'url': f'/web/content/?model=data.cleaner&id={self.id}&field=exportable_csv&filename=cleaned_csv.csv&download=true',
            'target': 'self',
        }