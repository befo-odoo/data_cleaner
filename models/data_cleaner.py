from odoo import api, fields, models
import csv
import base64
import io
class DataCleaner(models.Model):
    _name = 'data.cleaner'
    _description = 'Tool for importing and cleaning client data'
    
    file_loaded = fields.Boolean(string="File Loaded", default=False)
    file = fields.Binary(string="Uploaded File")
    cleaned_csv = fields.Char(default='Test')
    exportable_csv = fields.Binary()

    @api.onchange('file')
    def _onchange_file(self):
        # Only trigger wizard if file is added, not removed
        if self.file:
            print('trigger wizard here')
            data = self.decode_file()
            self.env['cleaner.spec'].process_data(data)
            # Since a file was added, mark it as loaded
            self.file_loaded = True

    # Decode file data for processing
    def decode_file(self):
        buf = io.StringIO(base64.b64decode(self.file).decode('utf-8'))
        return csv.DictReader(buf)

    # Export the formatted file and set variables back to default
    def export_csv(self):
        res = self.download_cleaned_csv()
        self.file_loaded = False
        self.file = None
        return res

    # Generate the CSV file from the cleaned data and execute download
    def download_cleaned_csv(self):
        self.exportable_csv = base64.b64encode(bytes(self.cleaned_csv, encoding='utf8'))
        return {
            'name': 'FEC',
            'type': 'ir.actions.act_url',
            'url': f'/web/content/?model=data.cleaner&id={self.id}&field=exportable_csv&filename=cleaned_csv.csv&download=true',
            'target': 'self',
        }

    def action_open_wizard(self):
        return {
            'name': "Cleaner Spec",
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'cleaner.spec',
            'view_id': self.env.ref('data_cleaner.cleaner_spec_view)').id,
            'target': 'new',
                }