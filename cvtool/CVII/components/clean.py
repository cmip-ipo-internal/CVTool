from copy import deepcopy

from collections import OrderedDict
from jsonschema import validate
import cvtool.core as core
import cvtool.CV.meta as meta
from p_tqdm import p_map
from tqdm import tqdm
from pprint import pprint
from functools import partial



# Logging 'info' level message using 'core.stdout.log' function
logger = core.stdout.log('cleaner', level='info')



def run(cvloc,prefix,metadata):

    files = ['activity_id','experiment_id','sub_experiment_id'] 
    collection = {}
    for f in files:
        loc = f"{cvloc}{prefix}{f}.json"
        load = core.io.json_read(loc)[f]

        collection[f] = load 

    

    activity_id = []
    source_type = []
    sub_experiment_id = []
    
    for _,experiment in collection.get('experiment_id',{}).items():

        for a in ['activity_id','parent_activity_id']:
            activity_id.extend(experiment.get(a,[]))

        source_type.extend(experiment.get('additional_allowed_model_model_components',[]))

        source_type.extend(experiment.get('required_model_components',[]))

        sub_experiment_id.extend(experiment.get('sub_experiment_id',[]))


    activity_diff = set(collection['activity_id']) -  set(activity_id) - set(['no_parent'])
    if activity_diff :
        corrected = {**metadata,"activity_id":core.io.filter_dict(collection['activity_id'],list(activity_id))}

        loc = f"{cvloc}{prefix}activity_id.json"
        core.io.write(corrected,loc)

        print(f"corrected activites file: <removed> {activity_diff}")


    print(activity_diff,set(collection['activity_id']) ,  set(activity_id) )


    sub_experiment_diff = set(collection['sub_experiment_id']) -  set(sub_experiment_id) 
    if sub_experiment_diff :
        corrected = {**metadata,"sub_experiment_id":core.io.filter_dict(collection['sub_experiment_id'],list(sub_experiment_id))}

        loc = f"{cvloc}{prefix}sub_experiment_id.json"
        core.io.write(corrected,loc)

        print(f"corrected sub_experiment file: <removed> {activity_diff}")


    core.io.rm_older(cvloc,minutes = 2)
    


