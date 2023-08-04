from odoo import models, api, fields
class CleanerSpec(models.TransientModel):
    _name = 'cleaner.spec'
    _description = 'data cleaner specificiation'
    
    attrs = fields.One2many(
        string='Attributes', 
        comodel_name='cleaner.spec.val',
        inverse_name='val'
    )
    vals = fields.Many2many(
        string='Values', 
        comodel_name='cleaner.spec.attr', 
        relation='attr_val_pairs', 
        column1='value', 
        column2='attribute'
    )

    # Process dirty data into correct structure for exporting
    def process_data(self, data):
        # Group attributes by product:
        #
        # [
        #   prod1: {
        #       attr1: [val1, val2, val3],
        #       attr2: [val4, val5]
        #   },
        #   prod2: {
        #       attr1: [val1, val6, val7],
        #       attr2: [val5, val8]
        #   }
        # ]
        #
        return
    
    # Generate clean csv file for importing
    def generate_csv(self):
        return "test,test1"

class CleanerSpecColumn(models.Model):
    _name = 'cleaner.spec.column'
    _description = 'data cleaner specificiation column'

    column_type = fields.Selection([
        ('attribute', 'Attribute'),
        ('none', 'Not an attribute')],
        string='Request Type')

    # Receive a column and process it
    def process_column(self, col_data):
        if self.column_type is 'attribute':
            return

class CleanerSpecAttr(models.Model):
    _name = 'cleaner.spec.attr'
    _description = 'cleaner specification attribute'
    attr = fields.Char(string='Attribute')

class CleanerSpecVal(models.Model):
    _name = 'cleaner.spec.val'
    _description = 'cleaner specification value'
    val = fields.Char(string='Value')