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
# It is the master list of everything that may processed in an order. 
# This does not have to correspond to the data fields we have entered. 
order = [
    #  stand alone 0 dependancy files go first (e.g. lisence etc. )
    'required_global_attributes',
    'source_id',
    'mip_era',
    'sub_experiment_id',
    # activity needs to come before experiments
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

        self.tempdir = core.io.mk_tempdir()
        print('Temporary directory stored at : '+ self.tempdir)

        core.io.copy_files(self.cvloc,self.tempdir)
        print('Successfully copied files from CVdir to Temporary Directory.')

        

        # push_output(repo_location,branch,source_location,prefix=self.prefix,overwrite=overwrite)

    def force_pull_CVs(self,overwrite=False):
        '''
        Use this function to ensure that our github CVs repository is current and most up to date. 
        
        '''
        pull_updates(self.cvloc,overwrite=overwrite)


    def process(self, updata):
        # file is the subheading, e.g. source_id
        metadata = meta.create(self.institution)

        for file in order:
            if file in updata:
                # debug(f'****************\n{file}\n**************')     

                module = import_script(*script_path(file,module='CVII')
                )
                current = updata[file]

                # loadcv = getattr(module, "loadcv", None)

                existing = module.load_existing(self.tempdir, self.prefix, parse = current.get('parse'))

                # debug('======================update')
                if 'update' in current:
                    existing = module.ammend(self.tempdir, self.prefix, existing,current.get('update'))

                # debug('======================exist')
                if 'add' in current:
                    existing = module.add_new(self.tempdir, self.prefix,existing,current.get('add'))



                existing = core.io.sort_dict(existing,reverse=False)
                complete = {**metadata,file:existing}
                
                
                core.io.json_write(complete,f'{self.tempdir}{self.prefix}{file}.json')

                print(self.tempdir)

        # remove any unused entries. These can be readded as-of and when they are needed. 
        clean = import_script(*script_path('clean',module='CVII'))
        clean.run(self.tempdir,self.prefix,metadata)

    def push(self,branch,overwrite= False):
        '''
        A function to force push the changes to a new branch. 
        '''
        push_output(self.cvloc,branch,self.tempdir,overwrite = overwrite)










##############################################
# getting data from CVs. CV.extract maybe?
##############################################

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
