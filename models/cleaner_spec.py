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
    rendering_trigger = fields.Boolean(string='Flag to rerender the wizard view', compute='_compute_rendering_trigger', default=False)

    # Fields to hold the values extracted from dirty data
    cols = fields.Char(string='Columns', default='')
    attrs = fields.Char(string='Attributes', default='')
    
    # Process dirty data into correct structure for exporting
    def process_data(self, sio):
        fields_view = self.env.ref('data_cleaner.view_cleaner_spec_form')
        arch = etree.fromstring(fields_view.arch)

        # Add all headers to the column list and strip undesired characters
        self.cols = sio.readline().replace('"', '').replace('\r\n', '')
        # Delete existing elements
        for old in arch.findall(".//*[@class='cleaner_spec_inl_el']"):
            arch.remove(old)
        for old in arch.findall(".//*[@name='onfirm_attr']"):
            arch.remove(old)
            
        # Build variable number of fields
        for index, field_name in enumerate(self.cols.split(','), start=1):
            button = etree.Element('button', {'class': f'cleaner_spec_inl_el btn-secondary button_{index}', 
                                                 'type': 'object', 
                                                 'name': 'confirm_attr', 
                                                 'string': 'Not Selected',
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

        # Toggle button status
        btn = arch.find(f".//button[@class='cleaner_spec_inl_el btn-secondary button_{index}']")
        if btn is not None:
            # Button currently not selected
            btn.set('string', 'Selected')
            classes = btn.get('class', '').split()
            classes.remove('btn-secondary')
            classes.append('btn-primary')
            btn.set('class', ' '.join(classes))
        else:
            # Button currently selected [@class='cleaner_spec_inl_el btn-primary button_{index}']
            btns = arch.findall(f".//button")
            btn = list(filter(lambda b: str(index) in b.attrib['class'], btns))[0]
            btn.set('string', 'Not selected')
            classes = btn.get('class', '').split()
            classes.remove('btn-primary')
            classes.append('btn-secondary')
            btn.set('class', ' '.join(classes))

        # Add attribute to attr list
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
    
    @api.depends('attrs')
    def _compute_rendering_trigger(self):
        self.rendering_trigger = not self.rendering_trigger

    # Update attribute list when form is saved
    def confirm_mappings(self):
        fields_view = self.env.ref('data_cleaner.view_cleaner_spec_form')
        arch = etree.fromstring(fields_view.arch)
        # Trigger if column header represents an attribute
        for element in arch.findall(".//*[@class='checked']"):
            if True: #element.get('checked') == 'checked':
                print(element.text)
                self.attrs += element + ','

        # Strip trailing commas
        self.attrs = self.attrs[:-1]

    def generate_csv(self, sio):
        return self._traverse_csv(sio, ['Vendor', 'Unit of Measure']) #TEST DATA with correct structure
        #return self._traverse_csv(sio, self.attrs)

    # Perform operations to clean the data
    def _traverse_csv(self, sio, attribute_array):
        print("Cleaning data")
        df = pd.read_csv(sio, sep="\t")
        new_col_list = [col_name for col_name in df.columns.values if col_name not in attribute_array]
        updated_col_list = new_col_list.copy()
        updated_col_list.extend(["Attribute", "Values"])
        df_dict = {c: [] for c in updated_col_list}
        for index, row in df.iterrows():
            print("Processing Row " + str(index))
            for col in new_col_list:
                df_dict[col].append(row[col])
            df_dict['Attribute'].append(attribute_array[0])
            df_dict['Values'].append(row[attribute_array[0]])
            for i in range(1, len(attribute_array)):
                df_dict['Attribute'].append(attribute_array[i])
                df_dict['Values'].append(row[attribute_array[i]])
                for col in new_col_list:
                    df_dict[col].append('')
                
        return pd.DataFrame(df_dict).to_csv()
    