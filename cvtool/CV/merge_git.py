

from typing import List, Dict, Any
from git import Repo
import os
from datetime import datetime
from .. import core

def pull_updates(repo_path, online_repo_url = 'https://github.com/WCRP-CMIP/CMIP6Plus_CVs.git', branch_name='main',overwrite=False):
    """
    Pull updates from an online Git repository into a local branch.
    
    Args:
        repo_path (str): Path to the local repository.
        online_repo_url (str): URL of the online repository.
        branch_name (str, optional): Name of the branch to pull updates into. Defaults to 'main'.
    """

    try:
        # Open the local repository
        repo = Repo(repo_path)

        
        # Add the online repository as a remote if it doesn't exist already
        if 'origin' not in repo.remotes:
            repo.create_remote('origin', online_repo_url)
        
        # Fetch updates from the online repository
        repo.remotes.origin.fetch()

        # Get the branch to pull updates into
        branch = f'{branch_name}'
        
        if overwrite:
            repo.git.stash('save', '-u')
            # repo.git.checkout('--', '.')
      
        # Check out the branch
        repo.git.checkout(branch)
 
        # Pull updates from the online repository into the local branch
        repo.remotes.origin.pull(branch)
        
        print(f'Updates from the online repository {repo_path} have been pulled into the local branch {branch}.')
    
    except Exception as e:
        print(f'An error occurred: {e}')







def push_output(repo_path,new_branch_name,source_directory,prefix='CMIP6Plus',overwrite = False) -> None:

    assert new_branch_name != 'main'

    # target_directory = repo_path
    repo = Repo(repo_path)
    if overwrite:
        repo.git.stash('save', '-u')
        # repo.git.checkout('--', '.')

    # Switch to the main branch and pull the latest updates
    repo.remotes.origin.pull('main')
    main_branch = repo.branches['main']
    main_branch.checkout()
    repo.remotes.origin.pull(new_branch_name)

# Check if the branch already exists
    if new_branch_name in [b.name for b in repo.branches]:
        # If the branch exists, check it out
        if overwrite:
            repo.git.branch('-D', new_branch_name)
            print(f'{new_branch_name} branch deleted and will be re-made.')
        else: 
            raise FileExistsError(f'The branch "{new_branch_name}" already exists in {repo_path}')
        # new_branch = repo.branches[new_branch_name]
        # new_branch.checkout()
        # # Pull latest changes to the EXISTING branch
        # try:
        #     repo.remotes.origin.pull(new_branch_name)
        # except:...
    # else:
        # If the branch doesn't exist, create it and check it out
            
    new_branch = repo.create_head(new_branch_name)
    new_branch.checkout()



    # Copy files from the source directory to the target directory in the new branch

    core.io.copy_files(source_directory,repo_path,prefix=prefix)

    # Stage, commit, and push the changes to the new branch
    # repo.index.add(target_directory)

    repo.git.add('--all')
    commit_message = f'Updating CVs for experiement {new_branch_name} - {datetime.now()}.'
    repo.index.commit(commit_message)
    check = input('Type "y" to push:\n')
    if check == "y":
        repo.git.push('--set-upstream', 'origin', new_branch_name)

        print(f'Updates pushed to the repository with commit {commit_message}')


