from odoo import api, fields, models

class DataCleaner(models.Model):
    _name = 'data.cleaner'
    _description = 'Tool for importing and cleaning client data'
    
    loaded = fields.Boolean(string="File Loaded", default=False)
    file = fields.Binary(string="Uploaded File")

    # Open a file and set its loaded status
    def import_csv(self):
        for record in self:
            record.file = None #TODO [upload and set file]
            record.loaded = True

    # Export the formatted file and set variables back to default
    def export_csv(self):
        for record in self:
            #TODO [download file here]
            record.file = None
            record.loaded = False