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
import git
from git import Repo
import tempfile
import glob
import os,json
from . import io
from .version_control import last_commit, query_repo, clear_last  # Assuming version_control is properly set up

__REPOPREFIX__ = 'cvtool.miptables.'

def setup_mip_tables(commit_hash = None) -> None:
    """
    Set up the MIP tables by checking for existing versions, downloading the latest version, and updating environment variables.
    """



    repo_url = 'https://github.com/PCMDI/mip-cmor-tables'


    # print('WARN WARN WARN WARN WARN WARN WARN WARN WARN WARN WARN - using wolfiex (test miptables) instead of PCMDI repo')
    # print('WARN WARN WARN WARN WARN WARN WARN WARN WARN WARN WARN - using wolfiex (test miptables) instead of PCMDI repo')
    # repo_url = 'https://github.com/wolfiex/mip-cmor-tables'

    table_subdir = ''

    term = io.terminal()
    print('*'*term.columns)

    if not commit_hash:
        # Get the last update from the GitHub repository
        current = last_commit(*repo_url.split('/')[-2:])
    else:
        current = dict(SHA=commit_hash)
        print(f'User specified MIPTABLE version')

    # The location of the system temporary files
    tmp = tempfile.gettempdir()
    repo = None

    # Check if we have any existing repositories in the tmp
    existing = glob.glob(f'{tmp}/{__REPOPREFIX__}*')


    for path in existing:
        t_repo = Repo(path)
        if str(t_repo.head.commit) == current.get('SHA') and t_repo.remotes.origin.url == repo_url:
            # Set the main repo as the existing one
            repo = t_repo
            existing.remove(path)

            # Remove the outdated duplicates if they exist
            for p in existing:
                io.rmdir(p)
            break

    if not repo:
        # If the repo does not exist or is not current, we download a new one.
        try:
            temp_dir = tempfile.mkdtemp(prefix=__REPOPREFIX__, suffix='')
        except FileExistsError:
            print("Directory already exists with the same name [this is unusual]")

        # Let's download the latest repository
        repo = Repo.clone_from(repo_url + '.git', temp_dir)

        # if we have specified a commit hash 
        if commit_hash:
            try:
                # Check if the commit exists
                commit = repo.commit(commit_hash)
                # Revert to the specified commit (creates a new commit)
                repo.git.reset('--hard', commit)

                print(f"Reverted to commit {commit_hash}")
            except git.exc.GitCommandError:
                print(f"Commit {commit_hash} not found in the repository.")
                print('WARN - using the latest version of the miptables instead.')

        if str(repo.head.commit) != current.get('SHA'):
            user = input(f"\n\nCommit messages: {str(repo.head.commit)} != {current.get('SHA')} \n This is likely because the MIPTable repository has been updated recently.\n\nType 'yes', to update the repository info and try again. \n\n")
            if user == 'yes':
                last = repo_url.split('/')[-2:]
                clear_last(*last)
                current = last_commit(*last)
            else:
                try:
                    # we revert to the last saved commit. 
                    commit_hash = current.get('SHA')
                    commit = repo.commit(commit_hash)
                    repo.git.reset('--hard', commit)
                    print(f"Reverted to commit {commit_hash}")
                except git.exc.GitCommandError:
                    print(f"Commit {commit_hash} not found in the repository.")


        assert str(repo.head.commit) == current.get('SHA'), 'Commit hashses must match. [core->MipTables]'

    # Get the repository URL
    repo_url = repo.remotes.origin.url
    # Get the current commit hash
    current_commit_hash = repo.head.commit.hexsha
    # Create clickable links
    repo_link = repo_url.replace(".git", "").replace(":", "/").replace("git@", "https://")
    commit_link = f"{repo_link}/commit/{current_commit_hash}"

    LOCATION = repo.working_dir + table_subdir
    # os.environ['cmor_tables'] = LOCATION
    # os.environ['cmor_tableorigin'] = commit_link

    miptables = query_repo(repo.working_dir)
    print('*'*term.columns)
    print(f"""
          MipTable location: {LOCATION} 
          With Commit: {current.get('SHA')}
          
          Latest Tag: {miptables['tag']['latest']}
          Latest Commit:{miptables['commit']['latest']}
          
          Viewable URL: {commit_link}

          """)
    print('*'*term.columns)


    institutions = json.load(open(f'{LOCATION}/MIP_institutions.json','r'))
    return miptables, LOCATION, institutions


