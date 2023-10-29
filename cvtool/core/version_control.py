'''
This file contains all the git, github and versioning functions for the cvtools library. 
'''

import requests
import subprocess
import os,re,glob
from typing import Dict
from .custom_errors import GitAPIError
from .io import read_temp, write_temp, exists, rm_temp
from git import Repo
from datetime import datetime


def last_commit(repo_owner: str, repo_name: str) -> Dict[str, str]:
    """
    Retrieve information about the latest commit of a GitHub repository.

    Args:
        repo_owner (str): Owner of the repository.
        repo_name (str): Repository name.

    Returns:
        dict: Dictionary containing details of the latest commit.
    """
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits"
    today_date = datetime.today().strftime("%Y%m%d")
    envname = f'cvtool.{repo_owner}.{repo_name}.{today_date}'
    commit_info = read_temp(envname)

    if commit_info:
        print(commit_info.get('api_url') , api_url)
        if commit_info.get('api_url') == api_url:
            print('Loading saved repo metadata from git.')
            return commit_info
    else:
        response = requests.get(api_url)
        if response.status_code == 200:
            commits_data = response.json()
            if commits_data:
                latest_commit = commits_data[0]
                commit_info = {
                    "api_url": api_url,
                    "SHA": latest_commit["sha"],
                    "Message": latest_commit["commit"]["message"],
                    "Author": f"{latest_commit['commit']['author']['name']} <{latest_commit['commit']['author']['email']}>",
                    "Committer": f"{latest_commit['commit']['committer']['name']} <{latest_commit['commit']['committer']['email']}>",
                    "Date": latest_commit["commit"]["author"]["date"]
                }
                write_temp(envname, commit_info)
                return commit_info
            else:
                raise GitAPIError(f"No commits found in the repository: {api_url}")
        else:
            raise GitAPIError(f"Failed to fetch commit information from the GitHub API: {api_url}")


def clear_last(repo_owner: str, repo_name: str) -> Dict[str, str]:
    today_date = datetime.today().strftime("%Y%m%d")
    envname = f'cvtool.{repo_owner}.{repo_name}.{today_date}'
    rm_temp(envname)


def git_user() -> Dict[str, str]:
    """
    Retrieve the Git username and email.

    Returns:
        dict: Dictionary containing 'user' and 'email' keys with corresponding values.
    """
    try:
        return get_user()
    except subprocess.CalledProcessError:
        return get_user(shell=True)

def get_github_version(repo_owner: str = '', repo_name: str = '') -> str:
    """
    Get the latest release version from GitHub API.

    Args:
        repo_owner (str): Owner of the repository.
        repo_name (str): Repository name.

    Returns:
        str: Latest release version or '-0.0.0' if not available.
    """
    if not repo_owner and not repo_name:
        if 'cmor_github_owner' in os.environ and 'cmor_github_repo' in os.environ:
            owner = os.environ['cmor_github_owner']
            repo = os.environ['cmor_github_repo']
        else:
            command = ["git", "config", "--get", "remote.origin.url"]
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
            output, _ = process.communicate()
            if process.returncode == 0:
                remote_url = output.strip()
                owner, repo = remote_url.split("/")[-2:]
                os.environ['cmor_github_owner'] = owner
                os.environ['cmor_github_repo'] = repo
            else:
                raise RuntimeError("Failed to get repository information.")

    try:
        today_date = datetime.today().strftime("%Y%m%d")
        envname = f'cvtool.{repo_owner}.{repo_name}.{today_date}'
        json_data = read_temp(envname)

        if not json_data or "tag_name" not in json_data: 
            api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"
            response = requests.get(api_url)
            response.raise_for_status()
            # GitAPIError(f"Failed to fetch commit information from the GitHub API: {api_url}")
            json_data = response.json()
            write_temp(envname, json_data)
          

        version = json_data.get("tag_name")
        return version if version else "-0.0.0"

        


    except (requests.RequestException, ValueError, IndexError) as e:
        print(f"Error: {str(e)}")
        return "-0.0.0"

def get_commit_hashes(owner: str, repo: str, latest: bool = True) -> str:
    """
    Get the latest or previous commit hash from GitHub API.

    Args:
        owner (str): Owner of the repository.
        repo (str): Repository name.
        latest (bool): True to get the latest commit hash, False to get the previous commit hash.

    Returns:
        str: Commit hash or None if failed to retrieve.
    """
    if 'cmor_github_hashes' in os.environ:
        hashes = os.environ['cmor_github_hashes'].split('~')
        return hashes[1 if latest else 0]
    else:
        try:
            api_url = f"https://api.github.com/repos/{owner}/{repo}/commits"
            response = requests.get(api_url)
            response.raise_for_status()
            json_data = response.json()

            latest_commit = json_data[0]["sha"]
            previous_commit = json_data[1]["sha"]

            os.environ['cmor_github_hashes'] = f"{previous_commit}~{latest_commit}"

            return latest_commit if latest else previous_commit
        except (requests.RequestException, ValueError, IndexError) as e:
            print(f"Error: {str(e)}")
            return None

def repo_commits(repo):
    """
    Print information about commits in a Git repository.

    Args:
        repo: Git repository object.
    """
    for commit in repo.iter_commits():
        print("Commit SHA:", commit.hexsha)
        print("Author:", commit.author.name, "<" + commit.author.email + ">")
        print("Committer:", commit.committer.name, "<" + commit.committer.email + ">")
        print("Date:", commit.authored_datetime)
        print("Message:", commit.message)
        print("-" * 50)




def query_repo(repo_path,verbose = True):

    exists(repo_path)
    repo = Repo(repo_path)

    # Get the current commit SHA
    current_commit = repo.head.object.hexsha

   # Get the latest tag version
    tags = repo.tags
    latest_tag = tags[-1]

   # Find the closest tag released prior to the target commit
    closest_previous_tag = None
    closest_distance = float('inf')

    for tag in repo.tags:
        tag_commit = repo.commit(tag.commit)
        distance = len(list(repo.iter_commits(rev=f'{tag_commit}..{current_commit}')))
        if distance < closest_distance:
            closest_distance = distance
            closest_previous_tag = tag


    # Get the current commit SHA
    current_commit = repo.head.object.hexsha

    # Check if the current commit is the latest commit
    is_latest_commit = current_commit == repo.heads[repo.active_branch.name].commit.hexsha

    # Get the repository URL
    repo_url = repo.remotes.origin.url

    # Check if there is a Zenodo DOI attached to the repository (assuming it's in the README file)
    zenodo_doi = None
    readme_path = os.path.join(repo_path, 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as readme_file:
            readme_content = readme_file.read()
            match = re.search(r'zenodo\.org/record/(\d+)', readme_content)
            if match:
                zenodo_doi = match.group(1)

    # Store the information in a dictionary
    if verbose:
        output_dict = {
            "tag":{
                "version": str(closest_previous_tag),
                "latest": latest_tag == closest_previous_tag,
            },
            "commit":{
                "SHA": current_commit,
                "latest": is_latest_commit,
            },
            "Repository URL": repo_url,
            "DOI": zenodo_doi
        }
    else:
        output_dict = {
            "tag":str(closest_previous_tag),
            "Repository URL": repo_url,
            "DOI": zenodo_doi
        }

    # license 

    license_files = glob.glob(os.path.join(repo_path, '*LICENSE*'))

    for license_file in license_files:
        try:

            if license_file == 'LICENSE':
                with open(license_file, 'r', encoding='utf-8') as file:
                    lines = file.readlines()
                    if len(lines) >= 3:
                        license_info = lines[2].strip()
                        if license_info:
                            output_dict['license'] = license_info
                            break  # Stop searching if a valid license is found
            else:
                output_dict['license'] = license_file
        except FileNotFoundError:
            print(f'License file {license_file} not found.')

    if 'license' not in output_dict:
        print('No valid license information found in the specified files.')

    return output_dict