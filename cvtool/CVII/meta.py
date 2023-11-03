import sys
import os

# Importing 'core' module from 'cvtool.core'
# core = sys.modules.get('cvtool.core')
# if not core:
#     sys.path.append('../../')
#     import core


cvtool = sys.modules.get('cvtool')
cvtool_version = cvtool.version
try:
    from cmor import CMOR_VERSION_MAJOR,CMOR_VERSION_MINOR,CMOR_VERSION_PATCH
    cmor_version = f"{CMOR_VERSION_MAJOR}.{CMOR_VERSION_MINOR}.{CMOR_VERSION_PATCH}"
except:
    cmor_version = "cmor python library not installed - version unknown"

import cvtool.core as core
# from cvtool.core.institutions import institutions , institutions_meta



tables = None

whoami = __file__.split('/')[-1].replace('.py','')


def create(institution, gitowner='WCRP-CMIP', gitrepo='CMIP6Plus_CVs', user=None):
    """
    Create a dictionary representing the header of a CV collection.

    Args:
        institution (str): The institution ID.
        gitowner (str): The owner of the Git repository (default: 'WCRP-CMIP').
        gitrepo (str): The name of the Git repository (default: 'CMIP6Plus_CVs').
        user (dict): User information dictionary (default: None).

    Returns:
        dict: A dictionary representing the header of the CV collection.

    """
    current_date = core.stdout.yymmdd()
    user = user or core.stdout.get_user()

    return {
        "Header": {
            "latest change":{
                "author": f'{user.get("user")} <{user.get("email")}>',
                "institution_id": institution,
            },
            "specs_doc": "v6.3.0 (link TBC)",
            "CMIP6Plus_CVS dir":{
                "CV_collection_modified": current_date,
                "CV_collection_version": core.version_control.get_github_version(gitowner, gitrepo),
                "previous_commit": core.version_control.get_github_version(gitowner, gitrepo),
            },
            "miptables":tables, 
            "CMOR":cmor_version,
            "CVTool":cvtool_version
            
        }
    }


def update(gitowner='WCRP-CMIP', gitrepo='CMIP6Plus_CVs'):
    '''
    Function to be used in combination with core.io.combine(optdata, overwrite).

    Args:
        gitowner (str): The owner of the Git repository (default: 'WCRP-CMIP').
        gitrepo (str): The name of the Git repository (default: 'CMIP6Plus_CVs').

    Returns:
        dict: A dictionary representing the header for updating the CV collection.

    '''
    user = core.stdout.get_user()
    current_date = core.stdout.yymmdd()

    return {
        "Header": {
            "CMIP6Plus_CVS dir":{
                 # 'updatetest': 'Yay! - to be removed.',
                "CV_collection_modified": current_date,
                "CV_collection_version": core.version_control.get_github_version(gitowner, gitrepo),
                "previous_commit": core.version_control.get_github_version(gitowner, gitrepo),
            },
            "latest change":{
                "author": f'{user.get("user")} <{user.get("email")}>',
                # "institution_id": institution,
            },
            "miptables":tables,
            "CMOR":cmor_version,
            "CVTool":cvtool_version
        }
    }
