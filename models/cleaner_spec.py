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
    

    # Fields to hold the values extracted from dirty data
    cols = fields.Char(string='Columns', default='')
    attrs = fields.Char(string='Attributes', default='')
    parent = fields.One2many(comodel_name='data.cleaner', inverse_name='specs', string='Parent Object')
    
    # Process dirty data into correct structure for exporting
    def process_data(self, sio):
        fields_view = self.env.ref('data_cleaner.view_cleaner_spec_form')
        arch = etree.fromstring(fields_view.arch)

        # Add all headers to the column list and strip undesired characters
        self.cols = sio.readline().replace('"', '').replace('\r\n', '')

        # Delete old existing elements
        for old in arch.findall(".//*[@class='cleaner_spec_inl_el']"):
            arch.remove(old)
        for old in arch.findall(".//*[@name='confirm_attr']"):
            arch.remove(old)
            
        # Build variable number of fields
        for index, field_name in enumerate(self.cols.split(','), start=1):
            button = etree.Element('button', {'class': f'cleaner_spec_inl_el btn-secondary button_{index}', 
                                                 'type': 'object', 
                                                 'name': 'confirm_attr', 
                                                 'string': 'Add',
                                                 'args': [index, field_name],
                                                })
            arch.append(button)
            label = etree.Element('h6', {'class': 'cleaner_spec_inl_el'})
            label.text = field_name
            arch.append(label)
            arch.append(etree.Element('br', {'class': 'cleaner_spec_inl_el'}))

        # Assign variable number of fields architecture to the view
        fields_view.arch = etree.tostring(arch)

    
    def confirm_attr(self, index, field):
        fields_view = self.env.ref('data_cleaner.view_cleaner_spec_form')
        arch = etree.fromstring(fields_view.arch)

        # Add attribute to attr list
        if field not in self.attrs:
            self.attrs += field + ','

        # Update view with changes
        fields_view.arch = etree.tostring(arch)

        return {
            'name': 'Select Columns that are Product Attributes',
            'type': 'ir.actions.act_window',
            'res_model': 'cleaner.spec',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
        }

    # Update attribute list when form is saved
    def confirm_mappings(self):
        self.parent.attrs = self.attrs

    def generate_csv(self, sio, attribute_array):
        print("Cleaning data")
        attribute_array = attribute_array.split(',')
        if attribute_array[-1] == '':
            attribute_array = attribute_array[:-1]
        df = pd.read_csv(sio, sep=",")
        if len(df.columns.values) == 1:
            all_cols = df.columns.values[0].split(',')
        else: #len(all_cols) > 1
            all_cols = df.columns.values
        new_col_list = [col_name for col_name in all_cols if col_name not in attribute_array]
        updated_col_list = new_col_list.copy()
        updated_col_list.extend(["Attribute", "Values"])
        df_dict = {c: [] for c in updated_col_list}
        for index, row in df.iterrows():
            print("Processing Row " + str(index))
            if len(row) == 1:
                row = {col: val for col,val in zip(row.keys()[0].split(','), row.keys()[0].split(','))}
            for col in new_col_list:
                df_dict[col].append(row[col])
            if len(attribute_array) > 0:
                df_dict['Attribute'].append(attribute_array[0])
                df_dict['Values'].append(row[attribute_array[0]])
            for i in range(1, len(attribute_array)):
                df_dict['Attribute'].append(attribute_array[i])
                df_dict['Values'].append(row[attribute_array[i]])
                for col in new_col_list:
                    df_dict[col].append('')
                
        return pd.DataFrame(df_dict).to_csv()
    