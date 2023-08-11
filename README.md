# Data Cleaner Tool

The Data Cleaner application is designed to automate the process of cleaning client data, specifically product variants (attributes and values)

## Usage

#### Installation

To access the data cleaner, the applicationr needs to be added to the ```--addons-path``` command line argument. Find the path of the parent diretory of where your ```data_cleaner``` is located, and append it to the ```--addons-path``` argument from where your instance of Odoo is started.

Next, install the ```data_cleaning``` module on your database from Apps.

#### Running the Tool

Once installed, the application can be opened. In the Data Cleaner application, upload a file, and then open the column mapping wizard by clicking the ```Map Fields``` button. Select all of the columns that are attributes, and then click ```Confirm``` to exit the wizard. Now, the file can be exported and all selected attributes will be formatted properly in the cleaned csv file.
