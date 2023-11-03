from copy import deepcopy

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
    key_pattern = r"^\w\d{4}$"
    description_pattern = r"^[A-Za-z0-9\-\. ]+$"
    
    return {
        "type": "object",
        "patternProperties": {
            key_pattern: {
                "type": "string",
                "pattern": description_pattern
            }
        },
        "additionalProperties": False
    }



def test(sub_experiments):

    
    for name, sub_exp in (pbar := tqdm(sub_experiments.items(),desc='')):
        
        pbar.set_description(f"Validating: {name}")
        # schema test
        try:
            validate(instance=sub_exp, schema=schema())
        except Exception as e:
            print(f"Validation failed:{name}  - {e}")

    pbar.set_description(f"Validation complete")

#########################
#  main

print('extract functions and use partial to import and redefine. ')

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

    assert not duplicates, f'Please remove duplicates from your sub_exp "add" section. \nYou can put them in the "update" to instead.\n Duplicates: {duplicates}'

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
