import logging
import requests
import subprocess
import json


def view(x):
    '''
    temporary json viewer
    '''
    import pprint
    pprint.pprint(x)

def log(name, level='info'):
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
    formatter = logging.Formatter(name + ': %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)

    # Add the console handler to the logger
    logger.addHandler(console_handler)

    return logger






def get_user(shell=False):
    """
    Retrieve the Git username and email.
    
    Args:
        shell (bool): Flag indicating whether to use shell execution for the subprocess command.
    
    Returns:
        dict: Dictionary containing 'user' and 'email' keys with the corresponding values.
    """
    # Command to retrieve the Git username
    username_command = ['git', 'config', '--global', 'user.name']
    username = subprocess.check_output(username_command, shell=shell, text=True).strip()

    # Command to retrieve the Git email
    email_command = ['git', 'config', '--global', 'user.email']
    email = subprocess.check_output(email_command, shell=shell, text=True).strip()

    return {'user': username, 'email': email}


def git_user():
    """
    Retrieve the Git username and email, handling subprocess errors.

    Returns:
        dict: Dictionary containing 'user' and 'email' keys with the corresponding values.
    """
    try:
        return get_user()
    except subprocess.CalledProcessError:
        return get_user(shell=True)


def yymmdd(delimiter='-'):
    """
    Get the current date in the format "YY-MM-DD" with a specified delimiter.

    Args:
        delimiter (str): Delimiter to separate the date components (default: '-').

    Returns:
        str: Current date in the format "YY-MM-DD".
    """
    from datetime import date
    current_date = date.today()
    formatted_date = current_date.strftime(f"%Y{delimiter}%m{delimiter}%d")
    return formatted_date





def get_github_version(owner,repo):
    try:
        

        if not owner and not repo:
            # Get the repository name and owner from the local .git directory
            command = ["git", "config", "--get", "remote.origin.url"]
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
            output, _ = process.communicate()
            if process.returncode != 0:
                raise RuntimeError("Failed to get repository information.")
            remote_url = output.strip().decode("utf-8")
            owner, repo = remote_url.split("/")[-2:]

        # Make a request to the GitHub API for the latest release
        api_url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
        response = requests.get(api_url)
        response.raise_for_status()
        json_data = response.json()
        version = json_data.get("tag_name")
        return version if version else "-0.0.0"
    except (subprocess.CalledProcessError, requests.RequestException, ValueError, IndexError) as e:
            print(f"Error: {str(e)}")
            return None



def get_commit_hashes(owner, repo ,latest = True):
    try:
        # Make a request to the GitHub API for the repository information
        api_url = f"https://api.github.com/repos/{owner}/{repo}/commits"
        response = requests.get(api_url)
        response.raise_for_status()
        json_data = response.json()

        # Extract the latest and previous commit hashes
        latest_commit = json_data[0]["sha"]
        previous_commit = json_data[1]["sha"]

        return  [previous_commit,latest_commit][latest]
    except (requests.RequestException, ValueError, IndexError) as e:
        print(f"Error: {str(e)}")
        return None