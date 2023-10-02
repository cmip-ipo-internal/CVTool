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
from typing import Optional, Dict, Callable


from .. import core
from ..core.miptables import setup_mip_tables #this will trigger the miptables import.

from ..core.dynamic_imports import load_module,import_script,script_path
from ..core.custom_errors import MipTableError

# from .components import meta
from . import meta



try:
    debug = sys.argv[1]
except IndexError:
    debug = False

if not debug:
    class PdbOver:
        def set_trace(self):
            pass
    pdb = PdbOver()
else:
    import pdb





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
    """
    Class for managing CV directory and file operations.
    """

    def __init__(self, prefix: str, base_files: list, **kwargs: Optional[Dict[str, str]]) -> None:
        """
        Initialize the CVDIR class.

        Args:
            prefix (str): Custom prefix for file names.
            base_files (list): List of base file names.
            **kwargs: Additional keyword arguments.
        """
        def config(name: str, default: str = '') -> str:
            if name in kwargs:
                print(f'Updating $cmor_{name} to {kwargs[name]}')
                os.environ['cmor_' + name] = kwargs[name]
            return os.environ.get('cmor_' + name, default)
        
        
        self.miptable_meta, self.tables = setup_mip_tables(commit_hash = config('MIPTABLE_SHA') or None)
        meta.tables = self.miptable_meta
    

        self.prefix = core.io.ensure_suffix(prefix, '_')
        self.directory = core.io.ensure_suffix(config('out_directory'), '/')
        self.file_names = base_files
        self.files = {}
        self.tables = config('tables') or self.tables
        if not self.tables: MipTableError(f'Table: "{self.tables}" not found in environmental variables "cmor+tables". This is usually generated from cvtool.core.miptables ')
        self.table_prefix = config('table_prefix')
        self.cvout = config('cvout', 'cv_cmor')

        core.io.exists(self.tables)

        if not core.io.exists(self.directory, False):

            self.create_project()

        for file_name in self.file_names:
            self.files[file_name] = core.io.json_read(
                os.path.join(self.directory, self.prefix + file_name))

    def create_project(self, base_files: Optional[list] = None) -> None:
        """
        Create the project by running the 'create' function from the parent module for each file.

        Args:
            base_files (list, optional): List of base file names. Defaults to None.
        """

        core.io.mkdir(self.directory)
        for file_name in self.files:
            output_name = file_name.split('.')[0]

            output_path = os.path.join(self.directory, output_name)

            # module_path = os.path.join(os.path.dirname(__file__), output_name)
            module_path = os.path.join(os.path.dirname(__file__),'components', output_name+'.py')


            file_path = os.path.join(self.directory, self.prefix + file_name)

            if not core.io.exists(file_path, False):
                if core.io.exists(output_path, False):
                    # module = importlib.import_module(module_path, output_name)
                        # loader = importlib.machinery.SourceFileLoader(output_name, module_path)
                        # module = loader.load_module()
                    import_script(output_name, module_path)
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

    def update_file(self, file_name: str, data: dict, update_func: Optional[Callable] = None) -> None:
        """
        Update a file with new data using the specified update function.

        Args:
            file_name (str): Name of the file.
            data (dict): New data to be updated in the file.
            update_func (callable, optional): Custom update function. Defaults to None.
        """
        output_name = file_name.split('.')[0]
        output_path = os.path.join(self.directory, output_name + '.json')

        # module = load_module(*basepath(file_name))
        module = import_script(*script_path(file_name))
        # import_script(*script_path(file_name))

        update_func = update_func or getattr(module, "preparse", None)
        if callable(update_func):
            preprocessed_data = self.pre_parse_update(file_name, data)
            data = update_func(self.files[file_name], preprocessed_data)

        # import inspect
        # print('**********',module,[member for member in inspect.getmembers(module) if inspect.isfunction(member[1])])


        if module:
            if not core.io.exists(output_path, error=False):
                jsn_data = module.create(data)
            else:
                jsn_data = json.load(open(output_path, 'r'))
                if not jsn_data:
                    print('empty:', file_name)
                    jsn_data = module.create(data)

            jsn_data = module.update(jsn_data, data)
        else:
            jsn_data = data

        core.io.json_write(jsn_data, output_path)

    def update_all(self, data: dict, opt_func: Optional[Dict[str, Callable]] = None) -> None:
        """
        Update all files with new data using the specified update functions.

        Args:
            data (dict): New data to be updated in the files.
            opt_func (dict, optional): Custom update functions. Defaults to None.
        """
        for key in global_keys:
            assert data.get('globals').get(
                key), f'Please provide {key} in the globals element'

        data['globals']['tables'] = self.tables
        data['globals']['table_prefix'] = self.table_prefix

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

        if opt_func is None:
            opt_func = {}

        for file_name in self.file_names:
            subdict = data.get(file_name) or dict()
            subdict['globals'] = data.get('globals')

            self.update_file(file_name, subdict,
                             opt_func.get(file_name) or None)

    def pre_parse_update(self, file_name: str, data: dict) -> dict:
        """
        Pre-process the update data before applying the update.

        Args:
            file_name (str): Name of the file.
            data (dict): New data to be updated in the file.

        Returns:
            dict: Pre-processed update data.
        """
        preprocessed_data = {}
        for key, value in data.items():
            preprocessed_data[f"{self.prefix}{key}"] = value
        return preprocessed_data

    def get_activity(self, activity: str = 'CMIP', external_path=None, aux = '') -> dict:
        """
        Get activity data.

        Args:
            activity (str, optional): Activity ID. Defaults to 'CMIP'.
            external_path (str, optional) A different table path to that which we are using (e.g. for mining CMIP3/5/6 tables) format: /path/to/tables/<PREFIX>
        Returns:
            dict: Activity data.
        """
        path = external_path or self.tables + self.table_prefix

        core.io.exists(f"{path}_CV.json")

        tabledata = core.io.json_read(f"{path}_CV.json", 'r')

        if 'CV' in tabledata:
            tabledata = tabledata['CV']

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

    def createCV(self, institution: str) -> None:
        """
        Create CV data.

        Args:
            institution (str): Institution name.
        """
        # from .components import compileCV
        compileCV = import_script(*script_path('compileCV'))
        cvloc = f"{self.directory}"
        cvfile = compileCV.create(
            self.directory, self.prefix, self.tables, outloc=self.cvout)
        print('check disabled')
        # self.checkCV(cvfile, institution)

    def checkCV(self, cvfile: str, institution: str) -> None:
        """
        Check CV data.

        Args:
            cvfile (str): CV file path.
            institution (str): Institution name.
        """
        from .. import CMORlib

        # self.tables = "/net/home/h03/hadmm/CDDS/github/CVTool/mip_specific/lesf/testdirLESF/cv_cmor/"
        # self.table_prefix = 'CMIP6Plus'


        # keep!
        # cmor_input = CMORlib.new_input.create(cvfile,
        #     self.prefix, 
        #     institution,
        #     tables=self.tables,
        #     table_prefix=self.table_prefix,
        #     writeLocation=cvfile.split(self.prefix)[0])
        

        #  cmor_input = CMORlib.new_input.create(cvfile,
        #     self.prefix, 
        #     institution,
        #     tables=self.tables,
        #     table_prefix=self.table_prefix,
        #     writeLocation=cvfile.split(self.prefix)[0])



        cmor_input = CMORlib.new_input.create(
            cvfile, self.prefix, institution, tables=self.tables, table_prefix=self.table_prefix,
            writeLocation=cvfile.split(self.prefix)[0],
            experiment_id='fut-Aer',
            sub_experiment_id='none',
            source_type='AOGCM',
            activity_id='LESFMIP',
            parent_activity_id='LESFMIP',
            parent_experiment_id='hist-Aer'
        )


        cmorclass = CMORlib.CMORise(self.tables, cmor_input)
        
        
        # cmorclass.process_data()
        print('cmor file created, not running tests since cmor misbehaves inside class. This is being addressed. ')

        print('lisence field needs editing to conform.')
        

        # print(cmor_input)


# class ProjectCreator:
#     """
#     Class for creating a project.
#     """

#     def __init__(self, prefix: str = '', directory: str = '', base_files: Optional[list] = None) -> None:
#         """
#         Initialize the ProjectCreator class.

#         Args:
#             prefix (str, optional): Custom prefix for file names. Defaults to an empty string.
#             directory (str, optional): Directory where parent modules reside. Defaults to an empty string.
#             base_files (list, optional): List of base file names. Defaults to None.
#         """
#         self.prefix = prefix
#         if not self.prefix.endswith('_'):
#             self.prefix += '_'
#         self.directory = directory
#         if not core.io.exists(directory, False):
#             os.makedirs(directory)
#         self.files = base_files or base

#     def create(self) -> None:
#         """
#         Create the project by running the 'create' function from the parent module for each file.
#         """
#         for file_name in self.files:
#             output_name = file_name.split('.')[0]
#             output_path = os.path.join(self.directory, output_name)
#             module_path = os.path.join(os.path.dirname(__file__), output_name)
#             file_path = os.path.join(self.directory, self.prefix + file_name)

#             if not core.io.exists(file_path, False):
#                 if core.io.exists(output_path, False):
#                     module = importlib.import_module(module_path, output_name)
#                     opt_func = opt_func or getattr(module, "create", None)

#                     if callable(opt_func):
#                         with open(file_path, 'w') as file:
#                             json.dump(opt_func(), file, sort_keys=True)
#                     else:
#                         print(
#                             f"Create function not implemented for {file_name}")
#             else:
#                 print(
#                     f"ERROR: No function provided for processing. Writing an empty file at {file_name}")

# Example usage
