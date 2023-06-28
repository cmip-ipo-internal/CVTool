import sys
import os

# Importing 'cvtool.core' and 'cvtool.CV.meta' modules
core = sys.modules.get('cvtool.core')
meta = sys.modules.get('cvtool.CV.meta')

# Extracting the parent directory name from the current file path
whoami = __file__.split('/')[-2]

# Logging 'info' level message using 'core.stdout.log' function
info = core.stdout.log(whoami, level='info')


def create(optdata):
    """
    Create a dictionary representing the header and content of a CV collection.

    Args:
        optdata (dict): Optional data dictionary.

    Returns:
        dict: A dictionary representing the header and content of the CV collection.

    """
    this = core.io.get_current_function_name()
    print(whoami, this)
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


    default_content = {
            "directory_path_example": "CMIP6Plus/CMIP/MOHC/HadGEM3-GC31-MM/historical/r1i1p1f3/Amon/tas/gn/v20191207/",
            "directory_path_sub_experiment_example": "CMIP6Plus/DCPP/MOHC/HadGEM3-GC31-MM/dcppA-hindcast/s1960-r1i1p1f2/Amon/tas/gn/v20200417/",
            "directory_path_template": "<mip_era>/<activity_id>/<institution_id>/<source_id>/<experiment_id>/<member_id>/<table_id>/<variable_id>/<grid_label>/<version>",
            "filename_example": "tas_Amon_HadGEM3-GC31-MM_historical_r1i1p1f3_gn_185001-186912.nc",
            "filename_sub_experiment_example": "tas_Amon_HadGEM3-GC31-MM_dcppA-hindcast_s1960-r1i1p1f2_gn_196011-196012.nc",
            "filename_template": "<variable_id>_<table_id>_<source_id>_<experiment_id >_<member_id>_<grid_label>[_<time_range>].nc"
        }


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
        info('Nothing to update')
        return None

    # Check if there is something to update
    assert len(jsn) >= 0

    # Update some of the metadata
    current_date = core.stdout.yymmdd()
    overwrite = meta.update()

    optdata = core.io.combine(optdata, overwrite)

    return core.io.combine(jsn, optdata)



