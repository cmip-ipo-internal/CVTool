import sys
sys.path.append('../../')
#  keep this 
import sys
import pdb
import cvtool
from cvtool import CV
from cvtool.core.stdout import view
import pandas as pd

sys.path.append('../../')

prefix = 'CMIP6Plus'
UPDATE_CVS = True


# Example usage
handler = CV.CVDIR(
    prefix=prefix,
    directory='testdirLESF',
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
    ],
    tables='/Users/daniel.ellis/WIPwork/cmip6-cmor-tables/Tables/',
    table_prefix='CMIP6',
)

# # Update all files with data using the example update function
if UPDATE_CVS:
    deck = handler.get_activity()
    damip = handler.get_activity(activity='DAMIP')

    '''
    Lets extract the names 
    '''

    df = pd.read_csv('./data/exp_in.csv')
    # omit the similarly named all but one experiments.
    df = df[~df['Name'].str.contains('abo')]

    experiments = {}

    damip_names = map(lambda x: x.lower(), damip['experiment_id'])

    for _, r in df.iterrows():
        name = r.Name
        if name.lower() in damip_names:
            #  existing historical
            entry = damip['experiment_id'][name].copy()
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
