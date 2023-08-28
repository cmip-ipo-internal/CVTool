

import requests

def last_commit(repo_owner,repo_name):
    '''
    Example Usage: 
        In [6]: last_commit(*repo_url.split('/')[-2:])
        Out[6]: 
        {'SHA': '9fa6eda52792b51326dfc77b955c4e46a8334a2c',
        'Message': 'Merge pull request #17 from PCMDI/issue16_durack1_addAcknowledgements\n\nadding acknowledgements',
        'Author': 'Paul J. Durack <me@pauldurack.com>',
        'Committer': 'GitHub <noreply@github.com>',
        'Date': '2023-07-21T21:37:57Z'}
    '''

    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits"

    response = requests.get(api_url)
    if response.status_code == 200:
        commits_data = response.json()
        if commits_data:
            latest_commit = commits_data[0]
            
            # Print information about the latest commit
            commit_info = {
                "SHA": latest_commit["sha"],
                "Message": latest_commit["commit"]["message"],
                "Author": latest_commit["commit"]["author"]["name"] + " <" + latest_commit["commit"]["author"]["email"] + ">",
                "Committer": latest_commit["commit"]["committer"]["name"] + " <" + latest_commit["commit"]["committer"]["email"] + ">",
                "Date": latest_commit["commit"]["author"]["date"]
            }

            return commit_info
        else:
            print("No commits found in the repository.")
    else:
        print("Failed to fetch commit information from the GitHub API.")


def git_user() -> dict:
    """
    Retrieve the Git username and email, handling subprocess errors.

    Returns:
        dict: Dictionary containing 'user' and 'email' keys with the corresponding values.
    """
    try:
        return get_user()
    except subprocess.CalledProcessError:
        return get_user(shell=True)


def get_github_version(owner: str = '', repo: str = '') -> str:
    """
    Get the latest release version from GitHub API.

    Args:
        owner (str): Owner of the repository.
        repo (str): Repository name.

    Returns:
        str: Latest release version or '-0.0.0' if not available.
    """
    if not owner and not repo:
        # Check if GitHub information is already stored in environment variables
        if 'cmor_github_owner' in os.environ and 'cmor_github_repo' in os.environ:
            owner = os.environ['cmor_github_owner']
            repo = os.environ['cmor_github_repo']
        else:
            # Get the repository name and owner from the local .git directory
            command = ["git", "config", "--get", "remote.origin.url"]
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
            output, _ = process.communicate()
            if process.returncode == 0:
                remote_url = output.strip()
                owner, repo = remote_url.split("/")[-2:]
                # Store the GitHub information in environment variables for future use
                os.environ['cmor_github_owner'] = owner
                os.environ['cmor_github_repo'] = repo
            else:
                raise RuntimeError("Failed to get repository information.")

    try:
        # Make a request to the GitHub API for the latest release
        api_url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
        response = requests.get(api_url)
        response.raise_for_status()
        json_data = response.json()
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
    # Check if GitHub information is already stored in environment variables
    if 'cmor_github_hashes' in os.environ:
        return os.environ['cmor_github_hashes'].split('~')['latest']
    else:
        try:
            # Make a request to the GitHub API for the repository information
            api_url = f"https://api.github.com/repos/{owner}/{repo}/commits"
            response = requests.get(api_url)
            response.raise_for_status()
            json_data = response.json()

            # Extract the latest and previous commit hashes
            latest_commit = json_data[0]["sha"]
            previous_commit = json_data[1]["sha"]

            os.environ['cmor_github_hashes'] = f"{previous_commit}~{latest_commit}"

            return latest_commit if latest else previous_commit
        except (requests.RequestException, ValueError, IndexError) as e:
            print(f"Error: {str(e)}")
            return None
        

def repo_commits(repo):
    for commit in repo.iter_commits():
        print("Commit SHA:", commit.hexsha)
        print("Author:", commit.author.name, "<" + commit.author.email + ">")
        print("Committer:", commit.committer.name, "<" + commit.committer.email + ">")
        print("Date:", commit.authored_datetime)
        print("Message:", commit.message)
        print("-" * 50)