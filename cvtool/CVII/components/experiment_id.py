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


# Logging 'info' level message using 'core.stdout.log' function
logger = core.stdout.log(whoami, level='info')

template = OrderedDict({
    # immediate identifiers
    "experiment_id": "",
    "activity_id": [],
    # experiment descriptors
    "experiment": "",
    "description": "",
    "start": 1700,
    "end": 2100,
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
            "start": {
                "anyOf": [
                    {"type": "integer", "minimum": 1700},
                    {"enum": ["none"]}
                ]
            },
            "end": {
                "anyOf": [
                    {"type": "integer", "maximum": 2100},
                    {"enum": ["none"]}
                ]
            },
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
            }
        },
        # "required": ["experiment_id", "activity_id", "experiment", "description", "start", "end", "sub_experiment_id", "parent_activity_id", "parent_experiment_id", "required_model_components", "additional_allowed_model_components", "tier"],
        "additionalProperties": False
    }


def check(key, compareset, experiment):
    if set(experiment.get(key)) - compareset:
        raise AssertionError(
            f"\n\nMissing value: {set(experiment.get(key)) - compareset} \n\n in column '{key}' \n\n for {experiment}")


def fix(exp):
  dummy = deepcopy(template)
  dummy.update(exp[1])

  dummy = core.stdout.listify(dummy,['parent_experiment_id','parent)sub_experiment_id','parent_activity_id','activity_id'])

  if not dummy.get('parent_experiment_id')[0] == None:
    dummy['parent_experiment_id'] = ['none']

  return exp[0],dummy



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
            print(f"Validation failed:{name}- {e}")


        # id
        assert name == experiment.get(
            'experiment_id'), 'Experiment names do not match: ' + name
    pbar.set_description(f"Validation complete")

#########################
#  main


def load_cv(cvloc, prefix, parse = None):
    fname = f"{cvloc}{prefix}{whoami}.json"
    core.io.exists(fname)
    experiments = dict(p_map(fix,core.io.json_read(fname)[whoami].items(),desc= 'standardising existing experiments',disable=True))
    if parse:
      experiments = parse(experiments)
    
    test(cvloc, prefix, experiments)
    return experiments
