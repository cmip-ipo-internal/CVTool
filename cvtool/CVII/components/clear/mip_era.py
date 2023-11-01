import sys
import os

# # Importing 'cvtool.core' and 'cvtool.CV.meta' modules
# core = sys.modules.get('cvtool.core')
# meta = sys.modules.get('cvtool.CV.meta')

# # Extracting the parent directory name from the current file path
# whoami = __file__.split('/')[-2]

import cvtool.core as core
import cvtool.CV.meta as meta
whoami = __file__.split('/')[-1].replace('.py','')

# Logging 'info' level message using 'core.stdout.log' function
logger = core.stdout.log(whoami, level='info')


def create(optdata):
    """
    Create a dictionary representing the header and content of a CV collection.

    Args:
        optdata (dict): Optional data dictionary.

    Returns:
        dict: A dictionary representing the header and content of the CV collection.

    """
    this = core.io.get_current_function_name()
    # print(whoami, this,optdata)

    institution = optdata['globals']['institution']

    optdata = optdata.get(this) or {}

    content = optdata.get('mipera')
  

    header = meta.create(institution)
    header[whoami] = content

    return header


def update(jsn, optdata):
    """
    Update the metadata of a CV collection.

    Args:
        jsn (dict): The existing CV collection dictionary.
        optdata (dict): Optional data dictionary.

    Returns:
        dict: The updated CV collection dictionary.

    """
    this = core.io.get_current_function_name()
    optdata = optdata.get(this)
    if not optdata:
        info('nothing to update')
        return jsn

    # Check if there is something to update
    assert len(jsn) >= 0

    # Update some of the metadata
    # current_date = core.stdout.yymmdd()
    overwrite = meta.update()

    optdata = core.io.combine(optdata, overwrite)

    return core.io.combine(jsn, optdata)
