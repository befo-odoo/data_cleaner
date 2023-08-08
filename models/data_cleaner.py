from odoo import api, fields, models
import csv
import base64
import io
import json
class DataCleaner(models.Model):
    _name = 'data.cleaner'
    _description = 'Tool for importing and cleaning client data'
    
    file_loaded = fields.Boolean(string="File Loaded", default=False)
    file = fields.Binary(string="Uploaded File")
    csv_data = fields.Char(string="Unformatted CSV Data")
    cleaned_csv = fields.Char(default='Test')
    exportable_csv = fields.Binary()

    # Update loaded status for field visibility
    @api.onchange('file')
    def _onchange_file(self):
        self.file_loaded = True if self.file else False

    # Load data and build wizard
    def open_wizard(self):
        serialized_data = json.dumps(list(self.decode_file()))
        wizard_view = self.env['ir.actions.act_window'].create({
            'name': 'data.mapping.wizard',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'cleaner.spec',
            'view_id': self.env.ref('data_cleaner.view_cleaner_spec_form').id,
            'context': {'data': serialized_data},
            'target': 'new',
        })
        spec = self.env['cleaner.spec'].create({})
        spec.process_data()
        return wizard_view

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

    # def action_open_wizard(self):
    #     return {
    #         'name': "Cleaner Spec",
    #         'type': 'ir.actions.act_window',
    #         'view_type': 'form',
    #         'view_mode': 'form',
    #         'res_model': 'cleaner.spec',
    #         'view_id': self.env.ref('data_cleaner.cleaner_spec_view').id,
    #         'target': 'new',
    #     }