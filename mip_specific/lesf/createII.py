import sys, os, re, pdb
sys.path.append('../../')

import cvtool
from cvtool.core.stdout import view, listify, debug_print
from cvtool import CVII as CV

import pandas as pd


#  keep this

# print = debug_print


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


# we need a different table set for DAMIP (only)

if os.getlogin() in ['daniel.ellis', 'root']:
    # moved files in auxillary folder.
    CMIP6Tables4DAMIP = os.environ['HOME'] + \
        '/WIPwork/cmip6-cmor-tables/Tables/Auxillary/CMIP6'
    # this is the new repository
    CVLoc = os.environ['HOME']+'/WIPwork/CMIP6Plus_CVs/'
else:
    CMIP6Tables4DAMIP = os.environ['HOME'] + \
        '/CDDS/github/cmip6-cmor-tables/Tables/CMIP6'
    CVLoc = -1


num = re.compile('\d+')
def y(x): return int(num.findall(str(x))[0])

##############################################
# env variables
##############################################


def create_env():
    # This will be replaced by an external specified file.
    envdict = dict(out_directory='LESF_CVs', table_prefix='MIP', clean='True')
    #  MIPTABLE_SHA = '9fa6eda52792b51326dfc77b955c4e46a8334a2c'
    for key, val in envdict.items():
        os.environ['cmor_'+key] = val


create_env()


##############################################
# set defaults
##############################################
prefix = 'CMIP6Plus'

##############################################
#  intialise the handler
##############################################


# Example usage
handler = CV.CV_update(
    prefix, CVLoc
)


data = {'experiment_id': {
    "parse": lambda d: {key: value for key, value in d.items() if 'DAMIP' not in value.get("activity_id", [])}

}, 'k': ''}

handler.update_all(data)


# ##############################################
# # optional additional updates - e.g. reading DAMIP
# ##############################################


# # # Update all files with data using the example update function
# if UPDATE_CVS:

#     deck = handler.get_activity(activity='CMIP', external_path=CMIP6Tables4DAMIP)

#     damip = handler.get_activity(activity='DAMIP',external_path=CMIP6Tables4DAMIP)

#     # lets solve the case issues when indexing by duplicating all.
#     #  there will be a more efficient way of doing this.
#     # Create a new dictionary to store modified values
#     new_damip = {}
#     damip_case = {}
#     for entry in damip:
#         damip_case[entry.lower()] = entry
#         new_damip[entry] = {}  # Create an empty dictionary for each entry
#         for key, value in damip[entry].items():
#             new_damip[entry][key.lower()] = value

#     # Update the original damip dictionary
#     damip = new_damip
#     del new_damip

#     '''
#     DRS
#     '''
#     DRS = cvtool.core.io.json_read(mergeLoc+'CMIP6Plus_DRS.json')['DRS']


#     '''
#     Lets extract the names
#     '''

#     df = pd.read_csv('./data/exp_in.csv')
#     # omit the similarly named all but one experiments.
#     df = df[~df['Name'].str.contains('abo')]

#     experiments = {}

#     damip_names = tuple(map(lambda x: x.lower(), damip['experiment_id']))

#     print('\nDAMIP contains:')
#     for i in damip_names:
#         print('\t-'+i)

#     print('\nLESEFMIP table extracted names(see lesef/data dir):')
#     for i in df.Name:
#         print('\t-'+i)

#     for _, r in df.iterrows():
#         name = r.Name


#         if name.lower() in damip_names:
#             # print('hist')

#             #  existing historical in damip
#             entry = damip['experiment_id'][name.lower()].copy()
#             entry['description'] = entry.get('description') or r.Description
#             entry['sub_experiment_id'] = ["f2023"]
#             entry['activity_id'] = ['LESFMIP']
#             # entry['parent_experiment_id'] = [damip_case.get(name,'no-parent')]
#             # if 'fut' in name.lower():


#         elif name.lower().replace('fut', 'hist') in damip_names:
#             # print('fut')
#             # if we are creating future occurances
#             entry = damip['experiment_id'][name.replace('fut', 'hist').lower()].copy()
#             entry['parent_experiment_id'] = [damip_case.get(name.replace('fut', 'hist'),'no-parent')]  # Not perfect as fut-ghg should have hist-GHG
#             entry['parent_activity_id'] = ['CMIP']
#             entry['experiment'] = entry['experiment'].replace(
#                 'historical', 'future')
#             entry['experiment_id'] = name
#             entry['description'] = entry.get('description') or r.Description
#             entry['activity_id'] = ['LESFMIP']

#         else:
#             # view(r.to_dict())
#             #  everything else unknown
#             entry = {}
#             entry['experiment'] = r.Experiment

#             entry['experiment_id'] = name
#             # entry['sub_experiment_id'] =  entry['sub_experiment_id']
#             entry['description'] = entry.get('description') or r.Description

#             print(f'Not in DAMIP[{name}]: {entry["experiment"]}-{entry["description"]}')

#         ####################
#         #  do this for all!
#         ####################


#         # activity info
#         entry['activity_id'] = entry.get('activity_id', ['LESFMIP'])
#         entry['parent_activity_id'] = entry.get('parent_activity_id',['CMIP'])

#         # dates and numbers
#         entry['tier'] = y(r.Tier)
#         entry['start'] = y(r['Start year'])
#         entry['end'] = y(r['End year'])

#         # if not existing add
#         entry['additional_allowed_model_components'] = 'AER CHEM BGC'.split() #entry.get('additional_allowed_model_components', 'AER CHEM BGC'.split())
#         entry['required_model_components'] = entry.get('required_model_components', ['AOGCM'])
#         entry['sub_experiment_id'] =  entry.get('sub_experiment_id',["f2023"])


#         experiments = listify(experiments,['parent_experiment_id','parent)sub_experiment_id','parent_activity_id'])
#         # print('-------', name)
#         experiments[name] = entry


#     print('Filtering out past1000, past2k')


#     experiments = {
#     key: value
#     for key, value in experiments.items()
#     if not any(parent_id in ['past1000', 'past2k'] for parent_id in value.get('parent_experiment_id', []))
#     }


#     # it atually comes from the deck
#     deck['experiment_id'] = {
#     key: value
#     for key, value in deck['experiment_id'].items()
#     if not any(parent_id in ['past1000', 'past2k'] for parent_id in value.get('parent_experiment_id', []))
#     }

#     # manual changes
#     for key in experiments:
#         if 'hist' in key:
#             experiments[key].update({'parent_activity_id':'CMIP','activity_id':'CMIP'})

#     experiments_to_remove = ['historical-cmip5', 'historical-ext', 'piControl-cmip5', '"piControl-spinup-cmip5"']
#     for experiment_id in experiments_to_remove:
#         deck['experiment_id'].pop(experiment_id, None)


# ##############################################
# #  start CV updates
# ##############################################

#     data = {
#         'globals': {
#             'institution': "CMIP-IPO",
#             'mergeLoc' : mergeLoc,
#             # 'merge':'all'
#         },
#         'mip_era': {
#             'create': {
#                 'mipera': prefix,
#                 # 'institution': 'testipo'
#             },
#             'update': {
#                 'updatedadd': 'topleveltest'
#             }
#         },
#         "DRS":{
#             "create":DRS
#         },
#         "activity_id": {
#             'create': {
#                 "activity_id": deck.get('activity_id')
#             },
#             'update': {
#                 "activity_id": {
#                     'LESFMIP': 'The Large Ensemble Single Forcing Model Intercomparison Project',
#                     'PMIP' : 'Paleoclimat Modeling Intercomparison Project',

#                 }
#             },
#             'merge':'all'
#         },
#         'experiment_id': {
#             'create': {
#                 'experiment_id': deck['experiment_id']
#             },
#             'update': {
#                 'experiment_id': experiments
#             }
#         },

#         'sub_experiment_id' : {
#             'create':{
#                 'sub_experiment_id':{
#                     'f2023': 'Forcings 2023',
#                     "none": "none"
#                 }
#             }
#         }
#     }

#     handler.update_all(data)

# # create the CV.json file in an out directory
# handler.createCV('CMIP-IPO')
# # merge with the existing CVs
# merge_location = handler.merge(CVtables = mergeLoc,prefix = 'CMIP6Plus')

# handler.createCV('CMIP-IPO',merge_location)

# # handler.createIni()


# # place the output files into the CV directory and push
# # handler.push(mergeLoc, branch = 'lesfmip', source_location = merge_location, overwrite=True)
