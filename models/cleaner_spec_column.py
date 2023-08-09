from odoo import fields, models

class CleanerSpecColumn(models.Model):
    _name = 'cleaner.spec.column'
    _description = 'cleaner spec column'

    text = fields.Char(string="Column Names")