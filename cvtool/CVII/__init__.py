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

    def __init__(self, prefix: str, CVLoc: str, **kwargs: Optional[Dict[str, str]]) -> None:

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

        core.io.exists(self.tables)
        core.io.exists(self.cvloc)

    def update_all(self, updata):
        # file is the subheading, e.g. source_id
        for file in order:
            if file in updata:


                module = import_script(*script_path(file,module='CVII')
                )
                # loadcv = getattr(module, "loadcv", None)
                



                existing = module.load_cv(self.cvloc, self.prefix, parse = updata[file].get('parse'))

                
