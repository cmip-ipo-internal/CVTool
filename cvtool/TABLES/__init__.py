
import json
import re
from test_functions import tests, ACCEPTED_VARS






class Table:
    def __init__(self, file_path)
        with open(file_path) as f:
            self.json_data = json.load(f)
    
    def add_variable(self, variable_name, variable_data):
        # perform checks on variable_data fields
        if not all(field in variable_data for field in ACCEPTED_VARS):
            raise ValueError('Missing field(s) in variable_data')
        
        for entry,value in variable_data.items():
            # ensure the new varaible matches the required conventions. 
            assert tests[entry](value)
        
        # add new variable
        self.json_data['variable_entry'][variable_name] = variable_data
        
    def save_json_file(self, file_path):
        with open(file_path, 'w') as f:
            json.dump(self.json_data, f, indent=4)






