import logging
import requests
import subprocess
import os
from datetime import date
import inspect

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

def listify(dictionary, keys):
    if not isinstance(keys, list): keys = [keys]
    for key in keys:
        if key in dictionary:
            if not isinstance(dictionary[key], list):
                dictionary[key] = [dictionary[key]]
    return dictionary




def debug_print(*args, **kwargs):
    ''' prints the file and line '''
    caller_frame = inspect.stack()[1]
    caller_file = '/'.join(caller_frame[1].split('/')[-2:])
    caller_line = caller_frame[2]

    print(*args, **kwargs)
    print(f"\033[92m^ [{caller_file}:{caller_line}]")
    print("\033[0m")
    

# # Replace the built-in print function with the custom print function
# print = core.stdout.custom_print
