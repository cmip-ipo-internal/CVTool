import json, ast

'''
Make changes to return error messages in addition to pass '''

def generic_check(PATH, value,kind):
    """
    Checks if all the items in the given value exist in the data.

    Args:
        PATH (str): The path to the file prefix.
        value (str): The value to be checked.

    Returns:
        bool: True if all items in the value exist in the data, False otherwise.
    """
    
    data = json.load(open(f'{PATH}_{kind}.json', 'r'))[kind]

    try:
        # safely eval strings into code. 
        val = ast.literal_eval(value)
    except:
        return False

    # Check if all items in val exist in data
    return all(item in data for item in val) 


def activity_id(PATH, value):
    return generic_check(PATH, value,'activity_id')

def additional_allowed_model_components(PATH, value):
    return generic_check(PATH, value,'source_type')

# def required_model_components (PATH,value):
#     return generic_check(PATH, value,'source_type')


def experiment_id(PATH, value):
    """
    Checks if all the items in the given value exist in the source_type data.

    Args:
        PATH (str): The path to the file prefix.
        value (str): The value to be checked.

    Returns:
        bool: True if all items in the value exist in the source_type data, False otherwise.
    """
       
    data = json.load(open(f'{PATH}_experiment_id.json', 'r'))['experiment_id']
    return value not in data


def min_number_yrs_per_sim(PATH,value):
    return int(value)>0



def parent_experiment_id(PATH, value):
    """
    Checks if all the items in the given value exist in the source_type data.

    Args:
        PATH (str): The path to the file prefix.
        value (str): The value to be checked.

    Returns:
        bool: True if all items in the value exist in the source_type data, False otherwise.
    """
       
    data = json.load(open(f'{PATH}_experiment_id.json', 'r'))['experiment_id']
    return value in data



