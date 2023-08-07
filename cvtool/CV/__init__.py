'''
This is where changes to CV files happen, and consequently the generated CV files (see CV submodule). 

We have the CVfile module - where the outpu t cv file is created
This is not that. 
The CV module manages changes and creation of initial files. 

'''

import json
import importlib.util
import os
import sys


# print(sys.modules)
from .. import core
from ..core.dynamic_imports import load_module
from . import meta

try:
    debug = sys.argv[1]
except:
    debug = False

if not debug:
    class pdbover:
        def set_trace(self):
            pass
    pdb = pdbover()
else:
    import pdb


def basepath(name, basepath=''):
    return __file__.replace('__init__', f'{basepath}{name}/__init__'), name


# mip = load_module(*basepath('mip_era'))

global_keys = ['institution']

base = [
    "DRS",
    "mip_era",
    "table_id",
    "activity_id",
    "nominal_resolution",
    "experiment_id",
    "realm",
    "_config.yml",
    "frequency",
    "required_global_attributes",
    "grid_label",
    "source_id",
    "mip_era",
    "institution_id",
    "source_type",
    "sub_experiment_id"
]


class CVDIR:
    def __init__(self, prefix='', directory='', base_files=None, tables='', table_prefix='', cvout=None):
        """
        Initializes the CVDIR class.

        Args:
            prefix (str): Custom prefix for file names. Default is an empty string.
            directory (str): Directory where parent modules reside. Default is an empty string.
            base_files (list): List of base file names. Default is None, which uses the 'base' list.
        """
        self.prefix = core.io.ensure_suffix(prefix, '_')
        self.directory = core.io.ensure_suffix(directory, '/')
        self.file_names = base_files or base
        self.files = {}
        self.tables = tables
        self.table_prefix = table_prefix
        self.cvout = cvout or 'cv_cmor'

        # ensure that the tables exist
        core.io.exists(tables)

        if not core.io.exists(directory, False):
            self.create_project()

        for file_name in self.file_names:
            self.files[file_name] = core.io.json_read(os.path.join(self.directory, self.prefix + file_name))

    def create_project(self, base_files=None):
        """
        Creates the project by calling the ProjectCreator class.

        Returns:
            ProjectCreator: Instance of the ProjectCreator class.
        """
        return ProjectCreator(self.prefix, self.directory, base_files).create()

    def update_file(self, file_name, data, update_func=None):
        """
        Updates a file with new data using the specified update function or the corresponding create function
        from the parent module.

        Args:
            file_name (str): Name of the file.
            data (dict): New data to be updated in the file.
            update_func (callable): Custom update function. If None, uses the create function from the parent module.
        """

        # pdb.set_trace()

        output_name = file_name.split('.')[0]
        output_path = os.path.join(self.directory, output_name+'.json')

        module = load_module(*basepath(file_name))
        # print(module,[*basepath(file_name)])

        # preparse the data
        update_func = update_func or getattr(module, "preparse", None)
        if callable(update_func):
            preprocessed_data = self.pre_parse_update(file_name, data)
            data = update_func(self.files[file_name], preprocessed_data)

            # self.files[file_name] = updated_data
            # file_path = os.path.join(self.directory, self.prefix + file_name)
            # with open(file_path, 'w') as file:
            #     json.dump(updated_data, file)

        if module:
            # processing functions need a create and an update.
            if not core.io.exists(output_path, error=False):
                pdb.set_trace()
                jsn_data = module.create(data)
            else:
                jsn_data = json.load(open(output_path, 'r'))
                if not jsn_data:
                    # empty files?
                    print('empty:', file_name)
                    jsn_data = module.create(data)
                # print(jsn_data)

            # update
            jsn_data = module.update(jsn_data, data)

        else:
            # the user wants to do something special.
            # code needs to be formatted within their update function.

            jsn_data = data

        # make a backup here!?
        core.io.json_write(jsn_data, output_path)

    def update_all(self, data, opt_func=None):
        """
        Creates all files with new data using the specified update function or the corresponding create functions
        from the parent modules.

        Args:
            data (dict): New data to be updated in the files.
            opt_func (callable): Custom update function.
        """

        #  ensure that the mandatory keys are contained.
        for key in global_keys:
            assert data.get('globals').get(
                key), f'Please provide {key} in the globals element'

        data['globals']['tables'] = self.tables
        data['globals']['table_prefix'] = self.table_prefix

        # if data == None:
        #     data = {}

        if opt_func is not None:
            if not isinstance(opt_func, dict):
                print(
                    "Warning: opt_func must be a dictionary of keys with corresponding values as functions or None.")
                opt_func = None
            else:
                for file_name, func in opt_func.items():
                    if not callable(func) and func is not None:
                        print(
                            f"Warning: value of key {file_name} must be a function or None. Changing this to None.")
                        opt_func[file_name] = None

        # we are doing a multi operation.
        if opt_func == None:
            opt_func = {}

        for file_name in self.file_names:
            # print(file_name, data.get(file_name) or None, opt_func.get(file_name) or None)

            subdict = data.get(file_name) or dict()
            subdict['globals'] = data.get('globals')

            self.update_file(file_name,  subdict,
                             opt_func.get(file_name) or None)

    def pre_parse_update(self, file_name, data):
        """
        Pre-parses the update data before applying the update.

        Args:
            file_name (str): Name of the file.
            data (dict): New data to be updated in the file.

        Returns:
            dict: Pre-processed update data.
        """
        # Add any pre-parsing logic here
        # Example: Prefixing keys with the custom prefix
        preprocessed_data = {}
        for key, value in data.items():
            preprocessed_data[f"{self.prefix}{key}"] = value
        return preprocessed_data

    def get_activity(self, activity='CMIP'):

        #  default = cmip deck 
        path = self.tables + self.table_prefix
        tabledata = core.io.json_read(f"{path}_CV.json", 'r')['CV']

        deck = {}
        deck['activity_id'] = {activity: tabledata['activity_id'][activity]}

        def filter_dict(data):
            if data:
                if isinstance(data, list):
                    return activity in data

                return {key: value for key, value in data.items() if
                    (isinstance(value, dict) and filter_dict(value.get('activity_id', ''))) or
                    (isinstance(value, str) and value == activity)} 
        
        experiments = tabledata['experiment_id']
        deck['experiment_id'] = filter_dict(experiments)

        return deck

    def createCV(self, institution):
        from . import compileCV
        # print(dir(compileCV))

        CVloc = f"{self.directory}"
        cvfile = compileCV.create(self.directory, self.prefix, self.tables, outloc=self.cvout)

        self.checkCV(cvfile, institution)

    def checkCV(self, cvfile, institution):
        from .. import CMORlib
        # MSM: Will need to be modified
        self.tables = "/net/home/h03/hadmm/CDDS/github/CVTool/mip_specific/lesf/testdirLESF/cv_cmor/"
        self.table_prefix='CMIP6Plus'
        cmor_input = CMORlib.new_input.create(
            cvfile, self.prefix, institution, tables=self.tables, table_prefix=self.table_prefix, 
            writeLocation=cvfile.split(self.prefix)[0], 
            # the following override defaults in the template
            experiment_id='fut-aer',
            sub_experiment_id='none',
            source_type='AOGCM',
            activity_id='LESFMIP',
            parent_activity_id='LESFMIP',
            parent_experiment_id='hist-aer'
            )

        # test the output 
        cmorclass = CMORlib.CMORise(self.tables, cmor_input)
        cmorclass.process_data()

        print(cmor_input)


class ProjectCreator:
    def __init__(self, prefix='', directory='', base_files=None):
        """
        Initializes the ProjectCreator class.

        Args:
            prefix (str): Custom prefix for file names. Default is an empty string.
            directory (str): Directory where parent modules reside. Default is an empty string.
        """
        self.prefix = prefix
        if not self.prefix.endswith('_'):
            self.prefix += '_'
        self.directory = directory
        if not os.path.exists(directory):
            os.makedirs(directory)
        self.files = base_files or base

    def create(self):
        """
        Creates the project by running the 'create' function from the parent module for each file.
        """
        for file_name in self.files:

            output_name = file_name.split('.')[0]
            output_path = os.path.join(self.directory, output_name)
            module_path = os.path.join(os.path.dirname(__file__), output_name)
            file_path = os.path.join(self.directory, self.prefix + file_name)

            if not os.path.exists(file_path):
                if os.path.exists(output_path):
                    module = importlib.import_module(module_path, output_name)
                    opt_func = opt_func or getattr(module, "create", None)

                    if callable(opt_func):
                        with open(file_path, 'w') as file:
                            json.dump(opt_func(), file, sort_keys=True)
                    else:
                        print(
                            f"Create function not implemented for {file_name}")
            else:
                print(
                    f"ERROR: No function provided for processing. Writing an empty file at {file_name}")


# # Example usage
# handler = CVDIR(prefix='MY_PREFIX', directory='path/to/modules', base_files=[
#     "DRS.json",
#     "mip_era.json",
#     "table_id.json"
# ])

# # Update all files with data using the example update function
# data = {}
# handler.update_all_files(data)
