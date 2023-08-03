from odoo import api, fields, models

class DataCleaner(models.Model):
    _name = 'data.cleaner'
    _description = 'Tool for importing and cleaning client data'
    
    model_type = fields.Many2one('ir.module.module', string='Name of Model', ondelete='cascade')
    file_upload = fields.Binary(string="Uploaded File")