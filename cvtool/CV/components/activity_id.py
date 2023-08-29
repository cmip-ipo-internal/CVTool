import sys
import os
import json

# Importing 'cvtool.core' and 'cvtool.CV.meta' modules
# core = sys.modules.get('cvtool.core')
# meta = sys.modules.get('cvtool.CV.meta')
import cvtool.core as core
import cvtool.CV.meta as meta
whoami = __file__.split('/')[-1].replace('.py','')


# Logging 'info' level message using 'core.stdout.log' function
logger = core.stdout.log(whoami, level='info')

default = None


def create(optdata):
    """
    Create a dictionary representing the header and content of a CV collection.

    Args:
        optdata (dict): Optional data dictionary.

    Returns:
        dict: A dictionary representing the header and content of the CV collection.

    """
    this = core.io.get_current_function_name()

    # get the globals before overwriting
    institution = optdata['globals']['institution']
    optdata = optdata.get(this) or {}

    content = optdata.get(whoami) # this may be different if the varaible does not reflect the file name (e.g. mip_era and mipera)
    institution = optdata.get('institution')

    header = meta.create(institution)
    header[whoami] = content or default

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
        logger.info('nothing to update')
        return jsn


    # Check if there is something to update
    assert len(jsn) >= 0

    # Update some of the metadata
    overwrite = meta.update()

    optdata = core.io.combine(optdata, overwrite)
    
    return core.io.combine(jsn, optdata)
