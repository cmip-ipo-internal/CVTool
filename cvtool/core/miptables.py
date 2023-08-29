'''
This file is set up such that importing it will run the relevant setup scripts.
*******
WARN: This does mean that once imported, it will not import again unless you start a new independent program.
*******

A module that manages the following:
 - checks for existing versions of the mip tables
 - downloading the latest version of the mip tables
 - saves these to the system temporary directory.

Requires: pip install GitPython

Todo:
- Replace print statements with logger

'''

from typing import List, Dict, Any
from git import Repo
import tempfile
import glob
import os
from . import io
from .version_control import last_commit  # Assuming version_control is properly set up

__REPOPREFIX__ = 'cmortool.miptables.'

def setup_mip_tables() -> None:
    """
    Set up the MIP tables by checking for existing versions, downloading the latest version, and updating environment variables.
    """
    repo_url = 'https://github.com/PCMDI/mip-cmor-tables'
    table_subdir = '/mip_cmor_tables/out/'

    # Get the last update from the GitHub repository
    current = last_commit(*repo_url.split('/')[-2:])

    # The location of the system temporary files
    tmp = tempfile.gettempdir()
    repo = None

    # Check if we have any existing repositories in the tmp
    existing = glob.glob(f'{tmp}/{__REPOPREFIX__}*')

    for path in existing:
        t_repo = Repo(path)
        if str(t_repo.head.commit) == current.get('SHA'):
            # Set the main repo as the existing one
            repo = t_repo
            existing.remove(path)

            # Remove the outdated duplicates if they exist
            for p in existing:
                io.rmdir(p)
            print('Created or updated the repository')
            break

    if not repo:
        # If the repo does not exist or is not current, we download a new one.
        try:
            temp_dir = tempfile.mkdtemp(prefix=__REPOPREFIX__, suffix='')
        except FileExistsError:
            print("Directory already exists with the same name [this is unusual]")

        # Let's download the latest repository
        repo = Repo.clone_from(repo_url + '.git', temp_dir)
        assert str(repo.head.commit) == current.get('SHA')

    # Get the repository URL
    repo_url = repo.remotes.origin.url
    # Get the current commit hash
    current_commit_hash = repo.head.commit.hexsha
    # Create clickable links
    repo_link = repo_url.replace(".git", "").replace(":", "/").replace("git@", "https://")
    commit_link = f"{repo_link}/commit/{current_commit_hash}"

    LOCATION = repo.working_dir + table_subdir
    os.environ['cmor_tables'] = LOCATION
    os.environ['cmor_tableorigin'] = commit_link

    print(f'MipTable location: {os.environ["cmor_tables"]} \norigin: {commit_link}')

# Run the setup function if the module is imported
setup_mip_tables()
