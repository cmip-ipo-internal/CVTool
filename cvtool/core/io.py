import os
import sys
import json

def exists(path, error=True):
    """
    Check if a given path exists.

    Args:
        path (str): The path to check.
        error (bool): Flag indicating whether to raise an error if the path does not exist.
    
    Returns:
        str or False: The path if it exists, False otherwise.
    
    Raises:
        FileNotFoundError: If the path does not exist and error is set to True.
    """
    if path:
        if not os.path.exists(path):
            if error:
                raise FileNotFoundError(f"The path '{path}' does not exist.")
            else:
                return False
        return path
    return False


def combine(new, old):
    """
    Combine two dictionaries.

    Args:
        new (dict): The new dictionary to merge.
        old (dict): The old dictionary to merge into.

    Returns:
        dict: The merged dictionary.
    """
    # merged_dict = old.copy()
    # merged_dict.update(new)
    # return merged_dict

    merged_dict = old.copy()
    for key, value in new.items():
        if key in merged_dict and isinstance(merged_dict[key], dict) and isinstance(value, dict):
            merged_dict[key] = combine(value, merged_dict[key])
        else:
            merged_dict[key] = value
    return merged_dict


def json_write(jsndata, filename, mode='w',sort=False):
    """
    Write JSON data to a file.

    Args:
        jsndata (dict): The JSON data to write.
        filename (str): The name of the file to write to.
        mode (str): The file mode (default is 'w' for write).

    Raises:
        IOError: If there is an error writing the JSON data to the file.
    """
    if filename [-5:] != '.json': 
        filename += '.json'
        
    with open(filename, mode) as file:
        json.dump(jsndata, file, indent=4,sort_keys=sort)

def json_read(file,mode='r'):
    return json.load(open(file,mode))



def get_current_function_name():
    import inspect
    current_frame = inspect.currentframe()
    caller_frame = inspect.getouterframes(current_frame)[1]
    function_name = caller_frame.function
    return function_name