'''
Functions for input-output operations within the cvtools library

'''

import os
import json
import shutil
import tempfile
import inspect
import glob
from typing import Union, Dict, Any

def exists(path: str, error: bool = True) -> Union[str, bool]:
    """
    Check if a given path exists.

    Args:
        path (str): The path to check.
        error (bool): Flag indicating whether to raise an error if the path does not exist.
    
    Returns:
        Union[str, bool]: The path if it exists, False otherwise.
    
    Raises:
        FileNotFoundError: If the path does not exist and error is set to True.
    """
    if path and not os.path.exists(path):
        if error:
            raise FileNotFoundError(f"The path '{path}' does not exist.")
        else:
            return False
    return path

def combine(new: dict, old: dict) -> dict:
    """
    Combine two dictionaries.

    Args:
        new (dict): The new dictionary to merge.
        old (dict): The old dictionary to merge into.

    Returns:
        dict: The merged_dict dictionary.
    """
    merged_dict = old.copy()
    for key, value in new.items():
        if key in merged_dict and isinstance(merged_dict[key], dict) and isinstance(value, dict):
            merged_dict[key] = combine(value, merged_dict[key])
        else:
            merged_dict[key] = value
    return merged_dict

def json_write(jsndata: dict, filename: str, mode: str = 'w', sort: bool = False) -> None:
    """
    Write JSON data to a file.

    Args:
        jsndata (dict): The JSON data to write.
        filename (str): The name of the file to write to.
        mode (str): The file mode (default is 'w' for write).
        sort (bool): Whether to sort the keys in the JSON output.

    Raises:
        IOError: If there is an error writing the JSON data to the file.
    """
    if not filename.endswith('.json'):
        filename += '.json'

    with open(filename, mode) as file:
        json.dump(jsndata, file, indent=4, sort_keys=sort)

def json_read(file_path: str, mode: str = 'r') -> dict:
    """
    Reads the contents of a JSON file.

    Args:
        file_path (str): Path to the JSON file.
        mode (str): The file mode (default is 'r' for read).

    Returns:
        dict: Contents of the file as a dictionary, or an empty dictionary if the file is not found.
    """
    try:
        with open(file_path, mode) as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def get_current_function_name() -> str:
    """
    Get the name of the calling function.

    Returns:
        str: The name of the calling function.
    """
    current_frame = inspect.currentframe()
    caller_frame = inspect.getouterframes(current_frame)[1]
    function_name = caller_frame.function
    return function_name

def ensure_suffix(var: str, end: str) -> str:
    """
    Ensure that a string ends with a specified suffix.

    Args:
        var (str): The input string.
        end (str): The suffix to ensure.

    Returns:
        str: The modified string with the ensured suffix.
    """
    if not var.endswith(end):
        var += end
    return var

def relpath(path: str, relto: str = None) -> str:
    """
    Get the relative path of a given path.

    Args:
        path (str): The path to get the relative path for.
        relto (str): The base path to make the path relative to (default is current working directory).

    Returns:
        str: The relative path of the input path.
    """
    abs_path = os.path.abspath(path)
    current_dir = relto or os.getcwd()
    return os.path.relpath(abs_path, current_dir)

def mkdir(directory_path: str) -> None:
    """
    Create a directory.

    Args:
        directory_path (str): The path of the directory to create.

    Raises:
        FileExistsError: If the directory already exists.
        Exception: If an error occurs while creating the directory.
    """
    try:
        os.mkdir(directory_path)
        print(f"Directory '{directory_path}' created successfully.")
    except FileExistsError:
        print(f"Directory '{directory_path}' already exists.")
    except Exception as e:
        print(f"An error occurred: {e}")

def rmdir(directory_path: str) -> None:
    """
    Remove a directory and its contents.

    Args:
        directory_path (str): The path of the directory to remove.

    Raises:
        Exception: If an error occurs while deleting the directory.
    """
    try:
        shutil.rmtree(directory_path)
        print(f"Removed directory: {directory_path}")
    except Exception as e:
        print(f"Error deleting directory {directory_path}: {e}")

def write_temp(prefix: str, content: dict) -> None:
    """
    Write content to a temporary JSON file.

    Args:
        prefix (str): The prefix for the temporary file name.
        content (dict): The content to write to the temporary file.
    """
    with tempfile.NamedTemporaryFile(mode='w', prefix=prefix, delete=False, suffix='.json') as temp_file:
        json.dump(content, temp_file, indent=4)

def read_temp(prefix: str, index: int = 0) -> dict:
    """
    Read content from a temporary JSON file.

    Args:
        prefix (str): The prefix of the temporary file name.
        index (int): The index of the temporary file to read from (default is 0).

    Returns:
        dict: The content read from the temporary file as a dictionary, or None if the file does not exist.
    """ 
    tmp = tempfile.gettempdir()
    existing = glob.glob(f'{tmp}/{prefix}*')

    if existing:
        with open(existing[index], 'r') as file:
            content = json.load(file)
            return content
        
    return None


def relative_to(absolte,current):
        
    absolute = os.path.abspath(absolte)
    # Get the absolute path of the current script
    current_script_path = os.path.abspath(current)

    # Calculate the relative path
    relative_path = os.path.relpath(absolte, current_script_path)

    return relative_path


def terminal():
    size = os.get_terminal_size()
    return size


def merge_dict(dict1, dict2, overwrite_keys=None):
    """
    Merge two dictionaries together.
    
    Args:
        dict1 (dict): First dictionary to merge.
        dict2 (dict): Second dictionary to merge.
        overwrite_keys (list): List of keys that are allowed to be overwritten if they exist in both dictionaries.

    ** dict 2 will overwrite values from dict one if those are allowed. 
    
    Returns:
        dict: Merged dictionary.
    
    Raises:
        ValueError: If any identical first-level keys are found and not included in overwrite_keys.
    """
    if overwrite_keys is None:
        overwrite_keys = set()

    conflicting_keys = False
    if overwrite_keys != 'all':
        common_keys = set(dict1) & set(dict2)
        conflicting_keys = common_keys - overwrite_keys
    
    if conflicting_keys:
        raise ValueError(f"Duplicate keys found: {', '.join(conflicting_keys)}. Use overwrite_keys list to allow overwriting or correct the error. ")
    
    # merged_dict = {**dict1, **dict2}

    merged_dict = dict(dict1)
    for key, value in dict2.items():
        if key in merged_dict and isinstance(merged_dict[key], dict) and isinstance(value, dict):
            merged_dict[key] = merge_dict(merged_dict[key], value, overwrite_keys)
        elif key in merged_dict and isinstance(merged_dict[key], list) and isinstance(value, list):
            merged_dict[key].extend(value)
            merged_dict[key] = list(set(merged_dict[key]))

        else:
            merged_dict[key] = value

    return merged_dict


def copy_files(src_dir, dest_dir, prefix=''):
    # Walk through the source directory
    for foldername, _, filenames in os.walk(src_dir):
        # Create corresponding folder in the destination directory
        dest_folder = dest_dir
        os.makedirs(dest_folder, exist_ok=True)
        
        # Copy files from the current folder to the destination folder
        for filename in filenames:
            # Add the specified prefix to individual files
            new_filename = prefix + filename
            src_file = os.path.join(foldername, filename)
            dest_file = os.path.join(dest_folder, new_filename)
            shutil.copy2(src_file, dest_file)  # Use shutil.copy2 to preserve metadata like timestamps

