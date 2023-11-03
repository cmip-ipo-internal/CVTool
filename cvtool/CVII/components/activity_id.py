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

template = OrderedDict()


# #################################
#  Tests
###################################


def schema():

    return {
    "type": "object",
    "properties": {
            "type": "object",
            "properties": {
                "long_name": {"type": "string", "pattern": "^[A-Za-z0-9\-\. ]+$"},
                "URL": {"type": "string", "format": "uri"}
            },
            "required": ["long_name", "URL"]
    },
    "required": ["long_name",'URL'],
    "additionalProperties": False
}




def test(activities):

    
    for name, activity in (pbar := tqdm(activities.items(),desc='')):
        
        pbar.set_description(f"Validating: {name}")
        # schema test
        try:
            validate(instance=activity, schema=schema())
        except Exception as e:
            print(f"Validation failed:{name}  - {e}")

    pbar.set_description(f"Validation complete")

#########################
#  main


def load_existing(cvloc, prefix, parse = None):
    fname = f"{cvloc}{prefix}{whoami}.json"
    core.io.exists(fname)
    load = core.io.json_read(fname)[whoami]
    
    if parse:
      load = parse(load)

    test(load)
    return load

def add_new(cvloc, prefix, existing ,new):
    duplicates = [new_item for new_item in new if new_item in existing]

    assert not duplicates, f'Please remove duplicates from your activity "add" section. \nYou can put them in the "update" to instead.\n Duplicates: {duplicates}'

    test(new)
    existing.update(new)
    return existing

def ammend(cvloc,prefix,existing,overwrite):
    
    # test the updated values
    ecopy = deepcopy(existing)
    ecopy.update(overwrite)
    test(ecopy)
    existing = core.io.merge_entries(existing,overwrite,append = False)
    return existing