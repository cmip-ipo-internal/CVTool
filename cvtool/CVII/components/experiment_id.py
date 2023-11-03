from copy import deepcopy
import sys
import os
import json
from collections import OrderedDict
from jsonschema import validate
import cvtool.core as core
import cvtool.CV.meta as meta
from p_tqdm import p_map
from tqdm import tqdm
whoami = __file__.split('/')[-1].replace('.py', '')
from pprint import pprint
from functools import partial



# Logging 'info' level message using 'core.stdout.log' function
logger = core.stdout.log(whoami, level='info')

template = OrderedDict({
    # immediate identifiers
    "experiment_id": "",
    "activity_id": [],
    # experiment descriptors
    "experiment": "",
    "description": "",
    "start": 'none',
    "end": 'none',
    'min_number_yrs_per_sim':0,
    # origin
    "sub_experiment_id": ["none"],
    "parent_activity_id": ["none"],
    "parent_experiment_id": ["none"],
    # components
    "required_model_components": [],
    "additional_allowed_model_components": [],
    "tier": 1
}
)


# #################################
#  Tests
###################################


def schema(activities):

    return {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {
            "experiment_id": {"type": "string"},
            "activity_id": {
                "type": "array",
                "items": {
                   "type": "string",
                   "enum": activities
                },
                "minItems": 1
            },
            "experiment": {"type": "string"},
            "description": {"type": "string"},
            # "start": {
            #     "anyOf": [
            #         {"type": "integer", "minimum": 1700},
            #         {"enum": ['none']}
            #     ]
            # },
            # "end": {
            #     "anyOf": [
            #         {"type": "integer", "maximum": 2100},
            #         {"enum": ['none']}
            #     ]
            # },
            "sub_experiment_id": {
                "type": "array",
                "items": {"type": "string"},
                "minItems": 1
            },
            "parent_activity_id": {
                "type": "array",
                "items": {
                    "type": "string",
                    "enum": activities
                },
                "minItems": 1
            },
            "parent_experiment_id": {
                "type": "array",
                "items": {"type": "string"},
                "minItems": 1
            },
            "required_model_components": {
                "type": "array",
                "items": {"type": "string"},
                "minItems": 1
            },
            "additional_allowed_model_components": {
                "type": "array",
                "items": {
                    "type": "string",
                    # "enum": source_type
                },
                "minItems": 0
            },
            "tier": {
                "type": "integer",
                "enum": [1, 2, 3]
            },
            "min_number_yrs_per_sim": {"type": "integer"}
        },
        "required": ["experiment_id", "activity_id", "experiment", "description", "start", "end", "sub_experiment_id", "parent_activity_id", "parent_experiment_id", "required_model_components", "additional_allowed_model_components", "tier"],
    }


def check(key, compareset, experiment):
    if set(experiment.get(key)) - compareset:
        raise AssertionError(
            f"\n\nMissing value: {set(experiment.get(key)) - compareset} \n\n in column '{key}' \n\n for {experiment}")


def fix(exp,update = False):
  dummy = deepcopy(template)
  dummy.update(exp[1])

  # lists
  dummy = core.stdout.listify(dummy,['parent_experiment_id','parent)sub_experiment_id','parent_activity_id','activity_id'])

  # integers
  for i in 'tier start end'.split(' '):
    # print(dummy[i],i )min_number_yrs_per_sim

    this = dummy[i]

    if isinstance(this, list):
      dummy[i] = this[0]

    if not this or this == '':
        dummy[i] = 'none'
        continue

    if this == 'none':
      continue

    dummy[i] = int(dummy[i]) or 'none'

  # nones
  if not dummy.get('parent_experiment_id')[0]:
    dummy['parent_experiment_id'] = ['none']


  if update: # dont return all new variables, just those we are changing. 
     dummy = core.io.filter_dict(dummy,exp[1])

  return exp[0],dummy


fix_update  = partial(fix, update=True)


def test(cvloc, prefix, experiments):

    # source_type = set(core.io.json_read(f"{cvloc}{prefix}source_type.json").get('source_type'))
    activity_id = list(set(core.io.json_read(f"{cvloc}{prefix}activity_id.json").get(
        'activity_id')).union(set(['no parent'])))

    for name, experiment in (pbar := tqdm(experiments.items(),desc='')):
        
        pbar.set_description(f"Validating: {name}")

        # schema test
        try:
            # Validate the JSON data against the schema
            validate(instance=experiment, schema=schema(
                activity_id))
            # print("Validation successful.")
            # print(f"{name} is valid. ")
        except Exception as e:
            print(f"Validation failed:{name}  - {e}")


        #  exp_id checker. If no eperiment_id is found, this is automatically true
        assert name == experiment.get(
            'experiment_id',name), 'Experiment names do not match: ' + name +experiment.get(
            'experiment_id') +'-'
    pbar.set_description(f"Validation complete")

#########################
#  main


def load_existing(cvloc, prefix, parse = None):
    fname = f"{cvloc}{prefix}{whoami}.json"
    core.io.exists(fname)
    load = dict(p_map(fix,core.io.json_read(fname)[whoami].items(),desc= 'standardising existing experiments',disable=True))

    
    if parse:
      load = parse(load)
      # pprint(experiments)
    
    test(cvloc, prefix, load)
    return load

def add_new(cvloc, prefix, existing ,new):

    duplicates = [new_item for new_item in new if new_item in existing]
    # any(new_item in existing for new_item in new)
    
    assert not duplicates, f'Please remove duplicates from your experiment "add" section. \nYou can put them in the "update" to instead.\n Duplicates: {duplicates}'


    new = dict(p_map(fix,new.items(),desc= 'standardising new experiments',disable=True))


    test(cvloc, prefix, new)
    existing.update(new)
    return existing

def ammend(cvloc,prefix,existing,overwrite):


    overwrite = dict(p_map(fix_update,overwrite.items(),desc= 'standardising overwriting experiments',disable=True))
    
    # test the updated values
    ecopy = deepcopy(existing)
    ecopy.update(overwrite)
    test(cvloc, prefix, ecopy)


    existing = core.io.merge_entries(existing,overwrite,append = False)
    return existing


# def append():
#    Where we add items
# is this needed, we can read and merge beforehand?
