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

    specs = fields.Many2one(comodel_name='cleaner.spec', string='Cleaner Specs')
    attrs = fields.Char(string='Spec Attributes', default='')
    
    # Update loaded status for field visibility
    @api.onchange('file')
    def _onchange_file(self):
        self.file_loaded = True if self.file else False

    # Load data and build wizard
    def open_wizard(self):
        self.ensure_one
        spec = self.env['cleaner.spec'].create({'parent': self})
        spec.process_data(self.decode_file())
        return {
            'name': 'Select Columns that are Product Attributes',
            'type': 'ir.actions.act_window',
            'res_model': 'cleaner.spec',
            'view_mode': 'form',
            'view_id': self.env.ref('data_cleaner.view_cleaner_spec_form').id,
            'res_id': spec.id,
            'target': 'new',
        }

    # Decode file data for processing
    def decode_file(self) -> StringIO:
        return StringIO(b64decode(self.file).decode('utf-8'))

    # Export the formatted file and set variables back to default
    def export_csv(self):
        spec = self.env['cleaner.spec'].search([('parent.id', '=', self.id)])
        self.cleaned_csv=spec.generate_csv(self.decode_file(), self.attrs)
        return self.download_cleaned_csv()

    # Generate the CSV file from the cleaned data and execute download
    def download_cleaned_csv(self):
        self.exportable_csv = b64encode(bytes(self.cleaned_csv, encoding='utf8'))
        return {
            'name': 'FEC',
            'type': 'ir.actions.act_url',
            'url': f'/web/content/?model=data.cleaner&id={self.id}&field=exportable_csv&filename=cleaned_csv.csv&download=true',
            'target': 'self',
        }