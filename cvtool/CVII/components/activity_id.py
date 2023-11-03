
from collections import OrderedDict
from jsonschema import validate
import cvtool.core as core
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

    return {
    "type": "object",
        "properties": {
            "long_name": {"type": "string", "pattern": "^[A-Za-z0-9\-\. ]+$"},
            "URL": {"type": "string", "format": "uri"},
        },
}




def test(activities):

    
    for name, activity in (pbar := tqdm(activities.items(),desc='')):
        
        pbar.set_description(f"Validating: {name}")
        # schema test
        try:
            validate(instance=activity, schema=schema())
        except Exception as e:
            print(f"Validation failed:{name}  - {e}")

        pbar.set_description(f"{whoami}")

#########################
#  main



load_existing = partial(generic_load_existing, whoami=whoami, test=test)
add_new = partial(generic_add_new, test=test)
ammend = partial(generic_ammend, test=test)
