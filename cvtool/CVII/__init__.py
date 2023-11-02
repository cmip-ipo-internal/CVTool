'''
This is where changes to CV files happen, and consequently the generated CV files (see CV submodule). 

We have the CVfile module - where the outpu t cv file is created
This is not that. 
The CV module manages changes and creation of initial files. 


data = { 'source_id': 
                {'add': adds new
                 'ammend': overwrites exisiting
                 'parse': applies a function to all existing
                 }
        }


'''
import json
import importlib.util
import os
import sys
from typing import Optional, Dict, Callable

from .. import core
# this will trigger the miptables import.
from ..core.miptables import setup_mip_tables
from ..core.dynamic_imports import load_module, import_script, script_path
from ..core.custom_errors import MipTableError
from .merge_git import pull_updates, push_output
# print = core.stdout.debug_print
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


# This is the order we compute the files.
order = [
    #  stand alone files go first (e.g. lisence etc. )
    'required_global_attributes',
    'source_id',
    'mip_era',
    'sub_experiment_id',
    'activity_id',
    'experiment_id'
]


class CV_update:
    """
    Class for managing CV directory and file operations.
    """

    def __init__(self, prefix: str, CVLoc: str, institution:str, **kwargs: Optional[Dict[str, str]]) -> None:

        def config(name: str, default: str = '') -> str:
            if name in kwargs:
                print(f'Updating $cmor_{name} to {kwargs[name]}')
                os.environ['cmor_' + name] = kwargs[name]
            return os.environ.get('cmor_' + name, default)

        self.cvloc = CVLoc

        self.miptable_meta, self.tables, self.institutions = setup_mip_tables(
            commit_hash=config('MIPTABLE_SHA') or None)
        # update the metadata file
        meta.tables = self.miptable_meta

        self.prefix = core.io.ensure_suffix(prefix, '_')

        self.files = {}
        # extract automatically from names in future.
        self.table_prefix = 'MIP'
        self.institution = institution

        core.io.exists(self.tables)
        core.io.exists(self.cvloc)

        

        # push_output(repo_location,branch,source_location,prefix=self.prefix,overwrite=overwrite)

    def force_pull_CVs(self,overwrite=False):
        pull_updates(self.cvloc,overwrite=overwrite)


    def process(self, updata):
        # file is the subheading, e.g. source_id
        for file in order:
            if file in updata:


                module = import_script(*script_path(file,module='CVII')
                )
                # loadcv = getattr(module, "loadcv", None)

                existing = module.load_existing(self.cvloc, self.prefix, parse = updata[file].get('parse'))

                print('======================exist')
                existing = module.add_new(self.cvloc, self.prefix,existing,updata[file].get('add'))

                print('======================update')
                final = module.ammend(self.cvloc, self.prefix, existing,updata[file].get('update'))


                complete = {'Header': meta.create(self.institution),file:final}


                core.io.json_write(complete,'experiments.json')
    












################
# other 
################


def get_activity(cvfile, activity: str = 'CMIP', ) -> dict:
        
        core.io.exists(cvfile)
        tabledata = core.io.json_read(cvfile, 'r')

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
