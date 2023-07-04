import sys
sys.path.append('../../')
#  keep this 
import pdb
import cvtool
# and then this 
from cvtool import CV
from cvtool.core.stdout import view

import pandas as pd

# from mymodule import myfunction


prefix = 'MY_PREFIX'


# Example usage
handler = CV.CVDIR(prefix=prefix, directory='testdir', base_files=[
    "mip_era",
    "DRS",
    "required_global_attributes",
    "license",
    "activity_id",
    "experiment_id"
], tables='/Users/daniel.ellis/WIPwork/mip-cmor-tables/Tables/', table_prefix='CMIP6Plus')

# # Update all files with data using the example update function


deck = handler.get_activity()
damip = handler.get_activity(activity='DAMIP')


'''
Lets extract the names 
'''

df = pd.read_csv('./data/exp_in.csv')
# omit the simarly named all but one experiments.
df = df[~df['Name'].str.contains('abo')]

experiments = {}

damip_names = map(lambda x: x.lower(), damip['experiment_id'])

for _, r in df.iterrows():
    name = r.Name
    if name.lower() in damip_names:
        #  existing historical
        entry = damip['experiment_id'][name].copy()
        # view(entry)
        # view(r.to_json())

        entry['activity_id'] = ['LESFMIP']
        entry['description'] = entry.get('description') or r.Description
        entry['tier'] = int(r.Tier)
        entry['start'] = int(r['Start year'])
        entry['end'] = int(r['End year'])

        experiments[name] = entry

    elif name.lower().replace('fut', 'hist') in damip_names:
        entry = damip['experiment_id'][name.replace('fut', 'hist')].copy()
        entry['experiment'] = entry['experiment'].replace(
            'historical', 'future')

        entry['activity_id'] = ['LESFMIP']
        entry['description'] = entry.get('description') or r.Description
        entry['experiment_id'] = name
        entry['tier'] = int(r.Tier)
        entry['start'] = (r['Start year'])
        entry['end'] = (r['End year'])

        experiments[name] = entry

    else:
        view(r.to_dict())
        print('^^^ missing')

        entry = {}
        entry['experiment'] = r.Experiment
        entry['description'] = entry.get('description') or r.Description
        entry['activity_id'] = ['LESFMIP']
        entry['experiment_id'] = name
        entry['tier'] = int(r.Tier)
        entry['start'] = (r['Start year'])
        entry['end'] = (r['End year'])

        experiments[name] = entry


# pdb.set_trace()

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
        'update': {
            'experiment_id': experiments
        }
    }
}


handler.update_all(data)


# CMOR
#  produce amon taz for a range of the experiments. (a representatice variable

# apmontas

# check that this works with an older version of CMOR? not versions.
# MM 3.7.1

# Set of tables - Put them on Jasmin.
# System that wraps around CMOR...


# activity id - cmip lesfmip
# the rest shoudl remain mainly the same .

# grid the same
#  list of tables is in the CVS file


#  generic CV needs to be kept consistant with table_id
#  might potentially break this down into single file field - in the same format as the CVS repo
# /Users/daniel.ellis/WIPwork/mip-cmor-tables/Tables/generic_CV.json

# esm- => emission driven versions


'''
sub experiement id 
 lesef mip future 
  
 subexp  start daate
 dcpp start date- run forwards, differet start = run forwards . 


 cmip , prublish as amip in subespeirment 
 seriesmp-r1-p1-f1

 make it work for cmor 

providence entry in the experiemtn - e.g. cmip 6 cmip ... historically x and y 

input 4 mips 

 

 only takes the 5 experimetns from CMIP 6 by DAMIP and own them. and adds the extra 7 experiment s

'''
