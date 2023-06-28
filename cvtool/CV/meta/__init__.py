import sys
import os

# Importing 'core' module from 'cvtool.core'
core = sys.modules.get('cvtool.core')
if not core:
    sys.path.append('../../')
    import core

# Extracting the parent directory name from the current file path
whoami = __file__.split('/')[-2]


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
            "CV_collection_modified": current_date,
            "CV_collection_version": core.stdout.get_github_version(gitowner, gitrepo),
            "author": f'{user.get("user")} <{user.get("email")}>',
            "checksum": "md5: EDITEDITEDITEDITEDITEDITEDITEDIT",
            "institution_id": institution,
            "previous_commit": core.stdout.get_github_version(gitowner, gitrepo),
            "specs_doc": "v6.3.0 (link TBC)"
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
            'updatetest': 'Yay! - to be removed.',
            "CV_collection_modified": current_date,
            "CV_collection_version": core.stdout.get_github_version(gitowner, gitrepo),
            "previous_commit": core.stdout.get_github_version(gitowner, gitrepo),
            "author": f'{user.get("user")} <{user.get("email")}>',
        }
    }
