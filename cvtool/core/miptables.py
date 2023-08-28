'''
This file is set up such that importing it will run the relevant setup scripts. 
*******
WARN: This does mean that once imported, it will not import again unless you start a new independant program. 
*******

A that manages the:
 - checks for existing versions of the mip tables
 - downloading the latest version of the miptables
 - saves these to the system temporary directory. 

 pip install GitPython

Todo 
- replace print with logger

'''
__REPOPREFIX__ = 'cmortool.miptables.'

from git import Repo
try:
    from version_control import last_commit 
except:
    from .version_control import last_commit 
import tempfile,glob,os
import io



repo_url = 'https://github.com/PCMDI/mip-cmor-tables'
table_subdir = '/mip_cmor_tables/out/'


# the location of the system temporary files
tmp = tempfile.gettempdir()
repo = False
# get the last update from the github repository
current = last_commit(*repo_url.split('/')[-2:])

# check if we have any existing repositories in the tmp
existing = glob.glob(f'{tmp}/{__REPOPREFIX__}*')

for path in existing:
    t_repo = Repo(path)
    print(t_repo)
    if str(t_repo.head.commit) == current.get('SHA'):
        # set the main repo as the existing one
        repo = t_repo
        existing.remove(path)

        # remove the outdated duplicates if they exist. 
        for p in existing:
            io.rmdir(p)

        print('Created, or updated the repository')
        break

if not repo:
    # if the repo does not exist, or is not current we download a new one. 
    try:
        temp_dir = tempfile.mkdtemp(prefix=__REPOPREFIX__,suffix='')
        # print("Temporary directory created:", temp_dir)
    except FileExistsError:
        print("Directory already exists with the same name [this is unusual]")

    #  lets download the latest repository
    repo = Repo.clone_from(repo_url+'.git', temp_dir)
    assert str(repo.head.commit) == current.get('SHA')




LOCATION = repo.working_dir + table_subdir
os.environ['cmor_tables'] = LOCATION
print(f'MipTable location: {os.environ["cmor_tables"]}')

