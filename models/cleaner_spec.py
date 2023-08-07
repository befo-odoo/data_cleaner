from odoo import models, api, fields
import pandas
class CleanerSpec(models.TransientModel):
    _name = 'cleaner.spec'
    _description = 'data cleaner specificiation'

    place = fields.Char()
    product_header = fields.Char(string="Product Header")
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
    #
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
    def process_data(self, data):
        # First, loop through all row headers and determine which stores the product, and which are attributes
        for header in data.fieldnames:
            if True:
                #trigger if column is product header
                self.product_header = header
            if True:
                #trigger if column is attribute
                self.attrs.write({'attr': header})
        
        return
    
    # Generate clean csv file for importing
    def generate_csv(self):
        return "test,test1"

class CleanerSpecColumn(models.Model):
    _name = 'cleaner.spec.column'
    _description = 'data cleaner specificiation column'

#     column_type = fields.Selection([
#         ('product_id', 'Product ID'),
#         ('attribute', 'Attribute'),
#         ('none', 'Not an attribute')],
#         string='Request Type')

#     # Receive a column and process it
#     def process_column(self, col_data):
#         if self.column_type == 'attribute':
#             return

class CleanerSpecAttr(models.Model):
    _name = 'cleaner.spec.attr'
    _description = 'cleaner specification attribute'
    attr = fields.Char(string='Attribute')

class CleanerSpecVal(models.Model):
    _name = 'cleaner.spec.val'
    _description = 'cleaner specification value'
    val = fields.Char(string='Value')
