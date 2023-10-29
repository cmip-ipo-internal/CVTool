''' Institutions are now in the mip tables. '''


# '''
# This file is set up such that importing it will run the relevant setup scripts.
# *******
# WARN: This does mean that once imported, it will not import again unless you start a new independent program.
# *******


# '''

# from typing import List, Dict, Any
# import git
# from git import Repo
# import tempfile
# import glob
# import os
# from . import io
# from .version_control import last_commit, query_repo  # Assuming version_control is properly set up

# __REPOPREFIX__ = 'cvtool.institutions.'


# repo_url = 'https://github.com/cmip-ipo-internal/CMIPInstitutions'


# term = io.terminal()

# # # we want the current only 
# # current = last_commit(*repo_url.split('/')[-2:])

# # The location of the system temporary files
# tmp = tempfile.gettempdir()
# repo = None

# # Check if we have any existing repositories in the tmp
# existing = glob.glob(f'{tmp}/{__REPOPREFIX__}*')


# for path in existing:
#     repo = Repo(path)
#     repo.remotes.origin.pull()
#     existing.remove(path)

#     # Remove the outdated duplicates if they exist
#     for p in existing:
#         io.rmdir(p)
#     break

# if not repo:
#     # If the repo does not exist or is not current, we download a new one.
#     try:
#         temp_dir = tempfile.mkdtemp(prefix=__REPOPREFIX__, suffix='')
#     except FileExistsError:
#         print("Directory already exists with the same name [this is unusual]")

#     # Let's download the latest repository
#     repo = Repo.clone_from(repo_url + '.git', temp_dir)



# # Get the repository URL
# repo_url = repo.remotes.origin.url
# # Get the current commit hash
# current_commit_hash = repo.head.commit.hexsha
# # Create clickable links
# repo_link = repo_url.replace(".git", "").replace(":", "/").replace("git@", "https://")
# commit_link = f"{repo_link}/commit/{current_commit_hash}"

# LOCATION = repo.working_dir

# institutions_meta = query_repo(repo.working_dir,False)
# print('*'*term.columns)
# print(f"""
#         Institution list: {LOCATION} 
#         Latest Tag: {institutions_meta['tag']}
#         Viewable URL: {commit_link}

#         """)
# print('*'*term.columns)

# import json
# institutions = json.load(open(f'{LOCATION}/institutions.json','r'))



