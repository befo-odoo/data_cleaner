from odoo import models, api, fields
from xml.etree import ElementTree as etree
from csv import DictReader
from io import StringIO
import json
import pandas as pd
import io


class CleanerSpec(models.TransientModel):
    _name = 'cleaner.spec'
    _description = 'data cleaner specificiation wizard'

    product_header = fields.Char(string="CSV Header for Product")
    cols = fields.Char(string='Columns', default='')
    attrs = fields.Char(string='Attributes', default='')
    vals = fields.Char(string='Values', default='')

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
    def process_data(self, data):
        self.process_headers(data)

    def process_headers(self, data):
        # Add variable number of column names to wizard
        # self.ensure_one()
        fields_view = self.env.ref('data_cleaner.view_cleaner_spec_form')
        arch = etree.fromstring(fields_view.arch)

        # Loop through all row headers and determine which stores the product, and which are attributes
        for header in data.fieldnames:
            # Trigger if column is product header
            if True: self.product_header = header
            # Trigger if column is attribute
            if True: self.attrs += header + ','
            # Add header to list of column names
            self.cols += header

        # Strip trailing comma
        self.attrs = self.attrs[:-1]

        for index, field_value in enumerate(self.cols, start=1):
            field_name = f'dynamic_field_{index}'
            field = etree.Element('field', {'name': field_name})
            arch.append(field)

        fields_view.arch = etree.tostring(arch)
        return

    # Generate clean csv file for importing
    def generate_csv(self, data):
        print("Cleaning data")
        df = pd.read_csv(data, sep="\t")
        attribute_array = ["Manufacturer",
                           "Collection",
                           "Color",
                           "Vendor_SKU",
                           "Designer",
                           "Fabric_Type",
                           "Fiber_Contents",
                           "Fabric_Width",
                           "Putup_Format"]
        new_col_list = [col_name for col_name in df.columns.values if col_name not in attribute_array]
        updated_col_list = new_col_list.copy()
        updated_col_list.extend(["Attribute", "Values"])
        updated_df = pd.DataFrame(columns=updated_col_list)
        j = 0
        for index, row in df.iterrows():
            print("Processing Row " + str(j))
            j = j + 1
            first_row = {col: row[col] for col in new_col_list}
            first_row['Attribute'] = attribute_array[0]
            first_row['Values'] = row[attribute_array[0]]
            updated_df = pd.concat([updated_df, pd.DataFrame([first_row])], ignore_index=True)
            for i in range(1, len(attribute_array)):
                temp_dict = {'Attribute': attribute_array[i], 'Values': row[attribute_array[i]]}
                updated_df = pd.concat([updated_df, pd.DataFrame([temp_dict])], ignore_index=True)
        return updated_df.to_csv(index=False)
