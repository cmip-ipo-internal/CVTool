import os, sys

def exists(path,error = True):
    if not os.path.exists(path):
        if error:
            raise FileNotFoundError(f"The path '{path}' does not exist.")
        else: return False
    return path
