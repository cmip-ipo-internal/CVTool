import logging
import requests
import subprocess
import os
from datetime import date


class MissingValueError(Exception):
    """
    Exception raised when a required value is missing.
    """
    pass


def view(x):
    '''
    Temporary JSON viewer.
    '''
    import pprint
    pprint.pprint(x)


def log(name: str, level: str = 'info') -> logging.Logger:
    # rename to configure_logger
    """
    Configure a logger with a console handler.

    Args:
        name (str): Name of the logger.
        level (str): Logging level (default: 'info').

    Returns:
        logging.Logger: Configured logger object.
    """
    # Create a logger instance with the specified name
    logger = logging.getLogger(name)
    logger.setLevel(logging.WARNING)  # Set the logger's level to WARNING

    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, level.upper()))  # Set the logging level for the console handler

    # Create a formatter and add it to the console handler
    formatter = logging.Formatter(f"{name}: %(levelname)s - %(message)s")
    console_handler.setFormatter(formatter)

    # Add the console handler to the logger
    logger.addHandler(console_handler)

    return logger

def yymmdd(delimiter='-'):
    """
    Get the current date in the format "YY-MM-DD" with a specified delimiter.

    Args:
        delimiter (str): Delimiter to separate the date components (default: '-').

    Returns:
        str: Current date in the format "YY-MM-DD".
    """
    current_date = date.today()
    formatted_date = current_date.strftime(f"%Y{delimiter}%m{delimiter}%d")
    return formatted_date


def get_user(shell: bool = False) -> dict:
    """
    Retrieve the Git username and email.

    Args:
        shell (bool): Flag indicating whether to use shell execution for the subprocess command.

    Returns:
        dict: Dictionary containing 'user' and 'email' keys with the corresponding values.
    """
    try:
        username = os.environ['cmor_username']
    except KeyError:
        username_command = ['git', 'config', '--global', 'user.name']
        username = subprocess.check_output(username_command, shell=shell, text=True).strip()
        os.environ['cmor_username'] = username

    try:
        email = os.environ['cmor_email']
    except KeyError:
        email_command = ['git', 'config', '--global', 'user.email']
        email = subprocess.check_output(email_command, shell=shell, text=True).strip()
        os.environ['cmor_email'] = email

    return {'user': username, 'email': email}


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


