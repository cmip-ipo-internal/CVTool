import sys, os, re, pdb
sys.path.append('../../')
import cvtool
from cvtool import CVII as CV 
import pandas as pd

if os.getlogin() in ['daniel.ellis', 'root']:
    # moved files in auxillary folder.
    CMIP6Tables4DAMIP = os.environ['HOME'] + \
        '/WIPwork/cmip6-cmor-tables/Tables/Auxillary/CMIP6'
else:
    CMIP6Tables4DAMIP = os.environ['HOME'] + \
        '/CDDS/github/cmip6-cmor-tables/Tables/CMIP6'


cvfile = f'{CMIP6Tables4DAMIP}_CV.json'



num = re.compile('\d+')
def y(x): return int(num.findall(str(x))[0])


def lesf ():
    damip = CV.get_activity(cvfile ,activity='DAMIP')

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

    # print('\nDAMIP contains:')
    # for i in damip_names:
    #     print('\t-'+i)

    # print('\nLESFMIPMIP table extracted names(see LESFMIP/data dir):')
    # for i in df.Name:
    #     print('\t-'+i)

    for _, r in df.iterrows():
        name = r.Name

        if name == 'historical':
            experiments['historical'] = {   "parent_activity_id": [
                "CMIP"
            ],
            "parent_experiment_id": [
                "piControl"
            ],
            "experiment": "all-forcing simulation of the recent past (CO2 concentration-driven)"}
            
            continue


        if name.lower() in damip_names:
            # print('hist')
            #  existing historical in damip
            entry = damip['experiment_id'][name.lower()].copy()

            entry['description'] = entry.get('description') or r.Description

            entry.update({'parent_activity_id':'CMIP','activity_id':'LESFMIP','parent_experiment_id': 'piControl',})



        elif name.lower().replace('fut', 'hist') in damip_names:
            # print('fut')
            # if we are creating future occurances
            entry = damip['experiment_id'][name.replace('fut', 'hist').lower()].copy()

            entry['experiment'] = entry['experiment'].replace(
                'historical', 'future')

            entry['experiment_id'] = name
            entry['description'] = entry.get('description') or r.Description

            entry.update({'parent_activity_id':'LESFMIP','activity_id':'LESFMIP','parent_experiment_id': name.replace('fut', 'hist')})


        else:
            # view(r.to_dict())
            #  everything else unknown
            entry = {}
            entry['experiment'] = r.Experiment or r.Description

            entry['experiment_id'] = name
            # entry['sub_experiment_id'] =  entry['sub_experiment_id']
            entry['description'] = entry.get('description') or r.Description

            entry.update({'parent_activity_id':'CMIP','activity_id':'LESFMIP','parent_experiment_id': 'piControl',})


            # print(f'Not in DAMIP[{name}]: {entry["experiment"]}-{entry["description"]}')

        ####################
        #  do this for all!
        ####################

        entry['sub_experiment_id'] = ["f2023"] 
        # dates and numbers
        entry['tier'] = y(r.Tier)
        entry['start'] = y(r['Start year'])
        entry['end'] = y(r['End year'])

        # if not existing add
        entry['additional_allowed_model_components'] = 'AER CHEM BGC'.split() 
        entry['required_model_components'] = entry.get('required_model_components', ['AOGCM'])
        

        experiments[name] = entry

    experiments = {
    key: value
    for key, value in experiments.items()
    if not any(parent_id in ['past1000', 'past2k'] for parent_id in value.get('parent_experiment_id', []))
    }


    # # it atually comes from the deck
    # deck['experiment_id'] = {
    # key: value
    # for key, value in deck['experiment_id'].items()
    # if not any(parent_id in ['past1000', 'past2k'] for parent_id in value.get('parent_experiment_id', []))
    # }


    # manual changes
    # for key in experiments:
    #     if 'hist' in key:
    #         experiments[key].update({'parent_activity_id':'CMIP','activity_id':'LESFMIP','parent_experiment_id': 'piControl',})


    # experiments_to_remove = ['historical-cmip5', 'historical-ext', 'piControl-cmip5', '"piControl-spinup-cmip5"']
    # for experiment_id in experiments_to_remove:
    #     # deck['experiment_id'].pop(experiment_id, None)
    #     experiments.pop(experiment_id, None)

    rm_suffix = '-ext -cmip5'.split()
    experiments = {key: value for key, value in experiments.items() if any(suffix not in key for suffix in rm_suffix)}


    '''
    <class 'AssertionError'> Please remove duplicates from your experiment "add" section. 
    You can put them in the "update" to instead.
    Duplicates: ['historical'] <traceback object at 0x1c90efd00>
    '''

    historical =  experiments.pop("historical", {})

    return dict(add=experiments,update = {'historical':historical})

if __name__ == '__main__':
    LESFMIP()