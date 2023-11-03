import sys, os, re, pdb
sys.path.append('../../')

import cvtool
from cvtool.core.stdout import view, listify, debug_print
from cvtool import CVII as CV

import pandas as pd
from get_experiments import lesf



##############################################
# open debugger on error
##############################################
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
branch = 'lesfII'

##############################################
#  intialise the handler
##############################################


# Example usage
handler = CV.CV_update(
    prefix, CVLoc, 'CMIP-IPO'
)

handler.force_pull_CVs(overwrite = True)
print(handler.cvloc)



# get the changed data. 
ldata = lesf()

keydict = { 'start_year':'start','end_year':'end'}

# sequence == load(parse) -> update -> add

fix_deck = {
                'amip':{'start':1979,'end':2022,'min_number_yrs_per_sim': 43},
                'esm-piControl':{'experiment':'pre-industrial control simulation with preindustrial CO2 emissions defined (CO2 emission-driven)'},
                'esm-hist':{'experiment':"all-forcing simulation of the recent past with atmospheric CO2 concentration calculated (CO2 emission-driven)"},
                'piControl':{'experiment' : "pre-industrial control (CO2 concentration-driven)"}

            }



data = {

        # experiments
        'experiment_id': {
                "add":ldata.get('add'),
                "update": {**ldata.get('update'),**fix_deck},
                "parse": lambda d: {key: {keydict.get(subkey,subkey):subvalue for subkey, subvalue in value.items()} for key, value in d.items() if (('DAMIP' not in value.get("activity_id", [])) and ( key.split('-')[-1] not in 'cmip5 ext'.split()))}

                    },

        # activites
        "activity_id": {
                "add":{"LESFMIP": {'long_name':"The Large Ensemble Single Forcing Model Intercomparison Project",'URL':"https://www.frontiersin.org/articles/10.3389/fclim.2022.955414/full"}
                },
                "update":{"CMIP": {'long_name':"CMIP DECK: 1pctCO2, abrupt4xCO2, amip, esm-piControl, esm-historical, historical, and piControl experiments",'URL':"https://gmd.copernicus.org/articles/9/1937/2016/gmd-9-1937-2016.pdf"}
                },
                "parse": lambda x: {list(x.keys())[0]: {'long_name': list(x.values())[0], 'URL': 'https://wcrp-cmip.org'}}

        },
        # sub experiments
        'sub_experiment_id':{
                "add":{'f2023': 'Forcings 2023'}
            }
    
}

handler.process(data)

handler.push(branch,overwrite=True)

