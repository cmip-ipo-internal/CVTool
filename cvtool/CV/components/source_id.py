import sys
import os
import json

import cvtool.core as core
import cvtool.CV.meta as meta
whoami = __file__.split('/')[-1].replace('.py','')

# Logging 'info' level message using 'core.stdout.log' function
logger = core.stdout.log(whoami, level='info')

default =  {
            "HadGEM3-GC31-LL":{
                "activity_participation":[
                    "CMIP"
                ],
                "cohort":[
                    "Published"
                ],
                "institution_id":[
                    "MOHC",
                    "NERC"
                ],
                "license_info":{
                    "exceptions_contact":"@metoffice.gov.uk <- cmip6.hadgem3",
                    "history":"2017-09-21: initially published under CC BY-SA 4.0; 2021-11-15: relaxed to CC BY 4.0",
                    "id":"CC BY 4.0",
                    "license":"Creative Commons Attribution 4.0 International License (CC BY 4.0; https://creativecommons.org/licenses/by/4.0/)",
                    "source_specific_info":"https://ukesm.ac.uk/licensing-of-met-office-nerc-and-niwa-cmip6-data/",
                    "url":"https://creativecommons.org/licenses/by/4.0/"
                },
                "source_id":"HadGEM3-GC31-LL",
                "source":"HadGEM3-GC31-LL (2016): aerosol:UKCA-GLOMAP-modeatmos:MetUM-HadGEM3-GA7.1 (N96; 192 x 144 longitude/latitude; 85 levels; top level 85 km)atmosChem:noneland:JULES-HadGEM3-GL7.1landIce:noneocean:NEMO-HadGEM3-GO6.0 (eORCA1 tripolar primarily 1 deg with meridional refinement down to 1/3 degree in the tropics; 360 x 330 longitude/latitude; 75 levels; top grid cell 0-1 m)ocnBgchem:noneseaIce:CICE-HadGEM3-GSI8 (eORCA1 tripolar primarily 1 deg; 360 x 330 longitude/latitude)"
            }
        }
# create a blank as it needs to be populated

    # default_content = json.load(open(f"{DRSpath}_CV.json",'r'))[whoami]

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
