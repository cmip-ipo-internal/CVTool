import logging, subprocess

# Configure logger
import logging

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
