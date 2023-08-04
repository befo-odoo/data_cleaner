from odoo import api, fields, models
import base64
class DataCleaner(models.Model):
    _name = 'data.cleaner'
    _description = 'Tool for importing and cleaning client data'
    
    file_loaded = fields.Boolean(string="File Loaded", default=True)
    file = fields.Binary(string="Uploaded File")
    cleaned_csv = fields.Char(default='Test')
    exportable_csv = fields.Binary()

    # Import a file, set its loaded status
    def import_csv(self):
        for record in self:
            record.file = None #TODO [upload and set file]
            # record.file_loaded = True

    # Export the formatted file and set variables back to default
    def export_csv(self):
        res = self.download_cleaned_csv()
        self.file = None
        # self.file_loaded = False
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