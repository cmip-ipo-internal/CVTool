import sys
import os
import json

# Importing 'cvtool.core' and 'cvtool.CV.meta' modules
core = sys.modules.get('cvtool.core')
meta = sys.modules.get('cvtool.CV.meta')

# Extracting the parent directory name from the current file path
whoami = __file__.split('/')[-2]

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
    print(whoami, this,optdata)
    institution = optdata['globals']['institution']
    print(optdata)
    DRSpath = optdata['globals']['tables']+ optdata['globals']['table_prefix']

  

    optdata = optdata.get(this) or {}
    # content = optdata.get(this)
    
    

    keys = [
    "directory_path_example",
    "directory_path_sub_experiment_example",
    "directory_path_template",
    "filename_example",
    "filename_sub_experiment_example",
    "filename_template"
    ]


    default_content = json.load(open(f"{DRSpath}_CV.json",'r'))[whoami]

    content = optdata.get('content') or default_content
    for k in keys: 
        assert k in content


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
        logger.info('Nothing to update')
        return jsn

    # Check if there is something to update
    assert len(jsn) >= 0

    # Update some of the metadata
    overwrite = meta.update()

    logger.INFO(overwrite)

    optdata = core.io.combine(optdata, overwrite)

    return core.io.combine(jsn, optdata)



