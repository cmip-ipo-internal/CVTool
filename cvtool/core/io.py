'''
Functions for input-output operations within the cvtools library

'''

import os
import json
import shutil
import tempfile
import inspect
import glob
import tempfile
import atexit
import shutil
import time
from typing import Union, Dict, Any, OrderedDict

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
        # print(f"Error deleting directory {directory_path}: {e}")
        ...

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

def rm_temp(prefix: str, index: int = 0) -> bool:
    """
    Remove a temporary file with the specified prefix and index.

    Args:
        prefix (str): The prefix of the temporary file name.
        index (int): The index of the temporary file to remove (default is 0).

    Returns:
        bool: True if the file was successfully removed, False otherwise.
    """
    tmp = tempfile.gettempdir()
    existing = glob.glob(f'{tmp}/{prefix}*')

    for tmpfl in existing: 
        try:
            os.remove(tmpfl)
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    return False




def mk_tempdir():
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()
    
    # Register a cleanup function to remove the temporary directory on program exit
    atexit.register(shutil.rmtree, temp_dir)
    
    # Return the path of the temporary directory
    return temp_dir+'/'


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

def filter_dict(input_dict, keys_to_keep):
    """
    Filters a dictionary to contain only key-value pairs with keys present in keys_to_keep list.
    
    Args:
        input_dict (dict): Input dictionary.
        keys_to_keep (list): List of keys to keep in the filtered dictionary.
        
    Returns:
        dict: Filtered dictionary containing only specified keys.
    """
    return {key: input_dict[key] for key in keys_to_keep if key in input_dict}

def sort_dict(d,reverse = False):
    """
    Recursively sort a dictionary by its keys, including nested dictionaries.

    Args:
        d (dict): Dictionary to be sorted.

    Returns:
        dict: Sorted dictionary.
    """
    if isinstance(d, dict):
        sorted_dict = OrderedDict()
        for key in sorted(d,reverse=reverse):
            sorted_dict[key] = sort_dict(d[key],reverse)
        return sorted_dict
    else:
        return d
    # return dict(sorted(d.items()))

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

def merge_entries(dict1, dict2, append=True):
    '''
    When we are merging multiple items

    append = true :: combines the values
    append =false :: replaces the values 

    '''
    common_keys = set(dict1) & set(dict2)
    for key in common_keys:
        if not append:
            # dict1[key] = dict1[key].update(dict2[key])

            # for k2 in dict2[key]:
            #     print(k2)
            #     dict1[key][k2] = dict2[key][k2]

            dict1[key] = {**dict1[key],**dict2[key]}
        else:
            dict1[key] = merge_dict(dict1[key],dict2[key],'all')

    return dict1
    



# def copy_files(src_dir, dest_dir, prefix=''):
#     # Walk through the source directory
#     for foldername, _, filenames in os.walk(src_dir):
#         # Create corresponding folder in the destination directory
#         dest_folder = dest_dir
#         mkdir(dest_folder)
        
#         # Copy files from the current folder to the destination folder
#         for filename in filenames:
#             # Add the specified prefix to individual files
#             new_filename = prefix + filename
#             src_file = os.path.join(foldername, filename)
#             dest_file = os.path.join(dest_folder, new_filename)
#             shutil.copy2(src_file, dest_file)  # Use shutil.copy2 to preserve metadata like timestamps


def copy_files(src_dir, dest_dir, prefix=''):
    # Create the destination directory if it doesn't exist
    os.makedirs(dest_dir, exist_ok=True)

    # Recursive function to handle nested directories and files
    def copy_recursive(src, dest):
        for item in os.listdir(src):
            src_item = os.path.join(src, item)

            dir_item = dest_item = os.path.join(dest, item)

            if prefix not in item:
                item = prefix+item

            dest_item = os.path.join(dest, item)
            
            if os.path.isdir(src_item):
                # If it's a directory, copy it recursively
                os.makedirs(dir_item, exist_ok=True)
                copy_recursive(src_item, dir_item)
            else:
                # If it's a file, copy it with the specified prefix
                shutil.copy2(src_item, dest_item)

    copy_recursive(src_dir, dest_dir)


def rm_older(directory_path,minutes = 5):
    current_time = time.time()
    five_minutes_ago = current_time - minutes * 60  # 5 minutes ago in seconds

    for foldername, subfolders, filenames in os.walk(directory_path):
        for filename in filenames:
            file_path = os.path.join(foldername, filename)
            # Get the last modification time of the file
            file_modified_time = os.path.getmtime(file_path)

            # Check if the file was not modified in the last 5 minutes
            if file_modified_time < five_minutes_ago:
                try:
                    # Remove the file
                    os.remove(file_path)
                    # print(f"Removed old file: {file_path}")
                except Exception as e:
                    print(f"Error occurred while removing file {file_path}: {e}")
