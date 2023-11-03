from copy import deepcopy

from collections import OrderedDict
from jsonschema import validate
import cvtool.core as core
from p_tqdm import p_map
from tqdm import tqdm
whoami = __file__.split('/')[-1].replace('.py', '')
from pprint import pprint
from functools import partial
from cvtool.CVII.components import * 

# Logging 'info' level message using 'core.stdout.log' function
logger = core.stdout.log(whoami, level='info')

template = OrderedDict()


# #################################
#  Tests
###################################


def schema():
    key_pattern = r"^(?:\w\d{4}|none)$"
    description_pattern = r"^[A-Za-z0-9\-\. ]+$"
    
    return {
        "type": "object",
        "patternProperties": {
            key_pattern: {
                "type": "string",
                "pattern": description_pattern
            }
        },
        # "additionalProperties": False
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


load_existing = partial(generic_load_existing, whoami=whoami, test=test)
add_new = partial(generic_add_new, test=test)
ammend = partial(generic_ammend, test=test)
