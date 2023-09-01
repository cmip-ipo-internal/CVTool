import sys,os,re
sys.path.append('../../')
#  keep this 
import pdb
import cvtool
from cvtool import CV
from cvtool.core.stdout import view
import pandas as pd

# we need a different table set for DAMIP (only)

if  os.getlogin() == 'daniel.ellis':
    CMIP6Tables4DAMIP = os.environ['HOME']+ '/WIPwork/cmip6-cmor-tables/Tables/CMIP6'
else:
    CMIP6Tables4DAMIP = os.environ['HOME']+ '/CDDS/github/cmip6-cmor-tables/Tables/CMIP6'



num = re.compile('\d+')
y = lambda x: int(num.findall(str(x))[0])

##############################################
# env variables
##############################################

def create_env():
    '''
    This will be replaced by an external specified file. 

    '''
    # mat
    # envdict = dict(out_directory='testdirLESF',tables='/home/h03/hadmm/CDDS/github/cmip6-cmor-tables/Tables/',table_prefix='CMIP6')

    # dan
    envdict = dict(out_directory='testdirLESF', table_prefix='CMIP6Plus')
    # tables=os.environ['HOME']+ '/WIPwork/cmip6-cmor-tables/Tables/'
    # !!!!!!!!!!!!!!!!!!!!!!!!!

    for key,val in envdict.items():
        print(key)
        os.environ['cmor_'+key] = val

create_env()



##############################################
# set defaults
##############################################

prefix = 'CMIP6Plus'
base_files=[
        "mip_era",
        "DRS",
        "required_global_attributes",
        "license",
        "activity_id",
        "experiment_id",
        "source_id",
        "sub_experiment_id",
        "further_info_url",
    ]


UPDATE_CVS = True


##############################################
#  intialise the handler
##############################################


# Example usage
handler = CV.CVDIR(
    prefix,
    base_files,
)


##############################################
# optional additional updates - e.g. reading DAMIP
##############################################


# # Update all files with data using the example update function
if UPDATE_CVS:

    deck = handler.get_activity()
    damip = handler.get_activity(activity='DAMIP',external_path=CMIP6Tables4DAMIP)

    # lets solve the case issues when indexing by duplicating all. 
    #  there will be a more efficient way of doing this. 
    # Create a new dictionary to store modified values
    new_damip = {}
    damip_case = {}
    for entry in damip:
        damip_case[entry.lower()] = entry
        new_damip[entry] = {}  # Create an empty dictionary for each entry
        for key, value in damip[entry].items():
            new_damip[entry][key.lower()] = value

    # Update the original damip dictionary
    damip = new_damip
    del new_damip


    '''
    Lets extract the names 
    '''

    df = pd.read_csv('./data/exp_in.csv')
    # omit the similarly named all but one experiments.
    df = df[~df['Name'].str.contains('abo')]

    experiments = {}

    damip_names = tuple(map(lambda x: x.lower(), damip['experiment_id']))

    print('\nDAMIP contains:')
    for i in damip_names:
        print('\t-'+i)

    print('\nLESEFMIP table extracted names(see lesef/data dir):')
    for i in df.Name:
        print('\t-'+i)

    for _, r in df.iterrows():
        name = r.Name


        if name.lower() in damip_names:
            # print('hist')

            #  existing historical in damip
            entry = damip['experiment_id'][name.lower()].copy()
            entry['description'] = entry.get('description') or r.Description

        elif name.lower().replace('fut', 'hist') in damip_names:
            # print('fut')
            # if we are creating future occurances
            entry = damip['experiment_id'][name.replace('fut', 'hist').lower()].copy()
            entry['parent_experiment_id'] = [damip_case.get(name.replace('fut', 'hist'))]  # Not perfect as fut-ghg should have hist-GHG
            entry['parent_activity_id'] = ['LESFMIP']
            entry['experiment'] = entry['experiment'].replace(
                'historical', 'future')
            entry['experiment_id'] = name
            entry['description'] = entry.get('description') or r.Description

        else:
            # view(r.to_dict())
            #  everything else unknown
            entry = {}
            entry['experiment'] = r.Experiment
            
            entry['experiment_id'] = name
            entry['sub_experiment_id'] =  ["none"] or entry['sub_experiment_id']
            entry['description'] = entry.get('description') or r.Description

            print(f'Not in DAMIP[{name}]: {entry["experiment"]}-{entry["description"]}')

        ####################
        #  do this for all! 
        ####################

        
        

        # activity info
        entry['activity_id'] = ['LESFMIP']
        entry['parent_activity_id'] = ['LESFMIP']

        # dates and numbers 
        entry['tier'] = y(r.Tier)
        entry['start'] = y(r['Start year'])
        entry['end'] = y(r['End year'])

        # if not existing add 
        entry['additional_allowed_model_components'] = 'AER CHEM BGC'.split() #entry.get('additional_allowed_model_components', 'AER CHEM BGC'.split())
        entry['required_model_components'] = entry.get('required_model_components', ['AOGCM'])
        entry['sub_experiment_id'] =  entry.get('sub_experiment_id',['none'])
        
        experiments[name] = entry


##############################################
#  start CV updates
##############################################

    data = {
        'globals': {
            'institution': "myInstitution"
        },
        'mip_era': {
            'create': {
                'mipera': prefix,
                'institution': 'testipo'
            },
            'update': {
                'updatedadd': 'topleveltest'
            }
        },
        "activity_id": {
            'create': {
                "activity_id": deck.get('activity_id')
            },
            'update': {
                "activity_id": {
                    'LESFMIP': 'The Large Ensemble Single Forcing Model Intercomparison Project'
                }
            }
        },
        'experiment_id': {
            'create': {
                'experiment_id': deck['experiment_id']
            },
            'update': {
                'experiment_id': experiments
            }
        }
    }

    handler.update_all(data)

# create the CV.json file in an out directory
handler.createCV('testinstitution')
