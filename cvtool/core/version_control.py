'''
This file contains all the git, github and versioning functions for the cvtools library. 
'''

import requests
import subprocess
import os
from typing import Dict
from .custom_errors import GitAPIError
from .io import read_temp, write_temp
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
