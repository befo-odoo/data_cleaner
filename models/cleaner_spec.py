from odoo import models, api, fields
from xml.etree import ElementTree as etree
from csv import DictReader
from io import StringIO
import json
import pandas as pd
import io

class CleanerSpec(models.Model):
    _name = 'cleaner.spec'
    _description = 'data cleaner specificiation wizard'
    
    parent = fields.One2many(comodel_name='data.cleaner', inverse_name='specs', string='Parent Object')

    # Fields to hold the values extracted from dirty data
    cols = fields.Char(string='Columns', default='')
    attrs = fields.Char(string='Attributes', default='')
    vals = fields.Char(string='Values', default='')
    
    # Process dirty data into correct structure for exporting
    def process_data(self, sio):
        fields_view = self.env.ref('data_cleaner.view_cleaner_spec_form')
        arch = etree.fromstring(fields_view.arch)

        # Add all headers to the column list and strip trailing comma
        line = sio.readline
        self.cols = sio.readline().split(',')
        self.cols = self.cols[:-1]

        #Delete existing elements
        for old in arch.findall(".//*[@class='cleaner_spec_inl_el']"):
            arch.remove(old)
            
        # Build variable number of fields
        for index, field_name in enumerate(self.cols.split(','), start=1):
            field = etree.Element('input', {'type': 'checkbox', 'id': f'attr{index}', 'class': 'cleaner_spec_inl_el'})
            arch.append(field)
            label = etree.Element('h6', {'class': 'cleaner_spec_inl_el'})
            label.text = field_name
            arch.append(label)
            arch.append(etree.Element('br', {'class': 'cleaner_spec_inl_el'}))

        # Assign variable number of fields architecture to the view
        fields_view.arch = etree.tostring(arch)

    # Update attribute list when form is saved
    def confirm_mappings(self):
        for header in self.cols:
            # Trigger if column header represents an attribute
            self.attrs += header + ','

        # Strip trailing commas
        self.attrs = self.attrs[:-1]

    def generate_csv(self, sio):
        return self._traverse_csv(sio, self.attrs, self.vals)

    # Perform operations to clean the data
    def _traverse_csv(self, sio, attribute_array, values_array):
        print("Cleaning data")
        df = pd.read_csv(sio, sep="\t")
        # attribute_array = ["Manufacturer",
        #                    "Collection",
        #                    "Color",
        #                    "Vendor_SKU",
        #                    "Designer",
        #                    "Fabric_Type",
        #                    "Fiber_Contents",
        #                    "Fabric_Width",
        #                    "Putup_Format"]
        new_col_list = [col_name for col_name in df.columns.values if col_name not in attribute_array]
        updated_col_list = new_col_list.copy()
        updated_col_list.extend(["Attribute", "Values"])
        df_dict = {c: [] for c in updated_col_list}
        for index, row in df.iterrows():
            print("Processing Row " + str(index))
            for col in new_col_list:
                df_dict[col].append(row[col])
            df_dict['Attribute'].append(attribute_array[0])
            df_dict['Values'].append(row[values_array[0]])
            # df_dict['Values'].append(row[attribute_array[0]])
            for i in range(1, len(attribute_array)):
                df_dict['Attribute'].append(attribute_array[i])
                df_dict['Values'].append(row[values_array[i]])
                # df_dict['Values'].append(row[attribute_array[i]])
                for col in new_col_list:
                    df_dict[col].append('')
                
        return pd.DataFrame(df_dict).to_csv()
    