import sys, os, re, pdb
sys.path.append('../../')

import cvtool
from cvtool.core.stdout import view, listify, debug_print
from cvtool import CVII as CV

import pandas as pd
from get_experiments import lesef


# debug on error
def custom_excepthook(type, value, traceback):
    print("\033[91m")

    print("An error occurred. Entering debugger.")
    print(type, value, traceback)
    # Print the full stack trace including file paths and line numbers
    print("\033[0m")
    pdb.post_mortem(traceback)


# Set custom excepthook
sys.excepthook = custom_excepthook



if os.getlogin() in ['daniel.ellis', 'root']:
    CVLoc = os.environ['HOME']+'/WIPwork/CMIP6Plus_CVs/'
else:
    CVLoc = -1


##############################################
# set defaults
##############################################
prefix = 'CMIP6Plus'
branch = 'lesefII'

##############################################
#  intialise the handler
##############################################


# Example usage
handler = CV.CV_update(
    prefix, CVLoc, 'CMIP-IPO'
)

handler.force_pull_CVs(overwrite = True)
print(handler.cvloc)

ldata = lesef()

keydict = { 'start_year':'start','end_year':'end'}

# sequence == load(parse) -> update -> add

data = {'experiment_id': {
            "add":ldata.get('add'),
            "update": ldata.get('update'),
            "parse": lambda d: {key: {keydict.get(subkey,subkey):subvalue for subkey, subvalue in value.items()} for key, value in d.items() if (('DAMIP' not in value.get("activity_id", [])) and ( key.split('-')[-1] not in 'cmip5 ext'.split()))}

            },
        "activity_id": {
                "add":{"LESFMIP": {'long_name':"The Large Ensemble Single Forcing Model Intercomparison Project",'URL':"https://www.frontiersin.org/articles/10.3389/fclim.2022.955414/full"}
                },
                "update":{"CMIP": {'long_name':"The Large Ensemble Single Forcing Model Intercomparison Project",'URL':"https://gmd.copernicus.org/articles/9/1937/2016/gmd-9-1937-2016.pdf"}
                },
                "parse": lambda x: dict(long_name=x,URL='none') 

        },
        'sub_experiment_id':{
            "add":{'f2023': 'Forcings 2023'}
            }
    
}
handler.process(data)


# handler.createCV('CMIP-IPO',merge_location)

# # handler.createIni()


# # place the output files into the CV directory and push
# # handler.push(mergeLoc, branch = 'lesfmip', source_location = merge_location, overwrite=True)
