from odoo import models, api, fields
from xml.etree import ElementTree as etree
from csv import DictReader
from io import StringIO
import json
class CleanerSpec(models.TransientModel):
    _name = 'cleaner.spec'
    _description = 'data cleaner specificiation wizard'

    product_header = fields.Char(string="CSV Header for Product")
    cols = fields.Char(string='Columns')
    attrs = fields.Char(string='Attributes')
    vals = fields.Char(string='Values')

    # Process dirty data into correct structure for exporting
    # Group attributes by product:
    # [
    #   prod1: {
    #       attr1: [val1, val2, val3],
    #       attr2: [val4, val5]
    #   },
    #   prod2: {
    #       attr1: [val1, val6, val7],
    #       attr2: [val5, val8]
    #   },
    # ]
    def process_data(self):
        serialized_data = r"{}".format(self.env['ir.actions.act_window'].search([('name', '=', 'data.mapping.wizard')]).context.replace("\'", "\""))
        data = DictReader(StringIO(json.loads(serialized_data)))
        self.process_headers(data)

    def process_headers(self, data):
        # Add variable number of column names to wizard
        self.ensure_one()
        fields_view = self.env.ref('data_cleaner.view_cleaner_spec_form')
        arch = etree.fromstring(fields_view.arch)

        # Loop through all row headers and determine which stores the product, and which are attributes
        for header in self.data.fieldnames:
            # Trigger if column is product header
            if True: self.product_header = header
            # Trigger if column is attribute
            if True: self.attrs.write({'attr': header})
            # Add header to list of column names
            self.cols.write(header)
        
        for index, field_value in enumerate(self.cols, start=1):
            field_name = f'dynamic_field_{index}'
            field = etree.Element('field', {'name': field_name})
            arch.append(field)

        fields_view.arch = etree.tostring(arch)
        return
    
    # Generate clean csv file for importing
    def generate_csv(self):
        return "test,test1"