import sys
import os


defaults = [
    "Conventions",
    "activity_id",
    "creation_date",
    "data_specs_version",
    "experiment",
    "experiment_id",
    "forcing_index",
    "frequency",
    "further_info_url",
    "grid",
    "grid_label",
    "initialization_index",
    "institution",
    "institution_id",
    "license",
    "mip_era",
    "nominal_resolution",
    "physics_index",
    "product",
    "realization_index",
    "realm",
    "source",
    "source_id",
    "source_type",
    "sub_experiment",
    "sub_experiment_id",
    "table_id",
    "tracking_id",
    "variable_id",
    "variant_label"
  ]


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

    # get the globals before overwriting
    institution = optdata['globals']['institution']
    optdata = optdata.get(this) or {}

    content = optdata.get(this) # this may be different if the varaible does not reflect the file name (e.g. mip_era and mipera)
    institution = optdata.get('institution')

    header = meta.create(institution)
    header[whoami] = content or defaults

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
