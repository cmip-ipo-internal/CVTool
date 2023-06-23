''' 
Scripts to dynamically import modules. 

Author and Maintainer: 
Daniel Ellis (daniel.ellis @ ext.esa.int)
'''

import importlib.abc
import importlib.util
import os 

class CustomLoader(importlib.abc.Loader):
    def __init__(self, path):
        self.path = path
    
    def exec_module(self, module):
        with open(self.path, 'r') as file:
            exec(file.read(), module.__dict__)

def load_module(absolute_path, module_name):
    '''
    Dynamically loads a module from the specified absolute path.

    Args:
        absolute_path (str): The absolute path of the module file.
        module_name (str): The desired name for the imported module.

    Returns:
        module: The imported module.

    Example:
        module = load_module('/path/to/my_module.py', 'my_module')
    '''
    try:
        module_spec = importlib.util.spec_from_file_location(module_name, os.path.abspath(absolute_path))
        module_spec.loader = CustomLoader(module_spec.origin)
        module = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(module)
        return module
    except Exception as e:
        print('ModuleLoadError', e)
        return None

def import_relative(__file__, module_name):
    '''
    Imports a relative module using the same process as load_module.

    Args:
        __file__ (str): The file name of the current module.
        module_name (str): The name of the relative module to import.

    Example:
        import_relative(__file__, 'etest')
    '''
    module_path = __file__.replace('__init__', module_name)
    module_spec = importlib.util.spec_from_file_location(module_name.replace('.', '_'), module_path)
    my_module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(my_module)
    globals()[module_name] = my_module


'''
# Example usage:
if __name__ == '__main__':
    # Load a module dynamically
    absolute_path = '/path/to/my_module.py'
    module_name = 'my_module'
    my_module = load_module(absolute_path, module_name)
    my_module.my_function()  # Assuming my_module has a function called my_function

    # Import a relative module
    import_relative(__file__, 'etest')
    etest.my_function()  # Assuming etest is the name of the relative module
'''