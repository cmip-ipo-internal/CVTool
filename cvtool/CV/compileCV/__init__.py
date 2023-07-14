''' 
Script to merge all the respective components of the CV directory.
''' 
import importlib.util
import os , re
from glob import glob
import shutil


from .variables import structure, template, source_type, frequencypattern, institutions

# from . import variables
# from variables import structure

import sys,os 
core = sys.modules.get('cvtool.core')


# print(dir(variables))

def create(directory,prefix,tables,outloc='cv_cmor'):
    
    cvdict = {'source_type':set()}
    missing = []


    if core.io.exists(f'{directory}{outloc}', False):
        # Delete the directory
        shutil.rmtree(f'{directory}{outloc}/')
    
    # create an empty directory
    os.mkdir(f'{directory}{outloc}/')

    for entry in structure: 
        file = f"{directory}{entry}.json"

        if entry == 'table_id':
            # print()
            # import pdb
            # pdb.set_trace()
            cvdict[entry] = sorted([os.path.basename(table.rstrip('.json')) for table in glob(tables+'*') if re.search(frequencypattern, table) and '.json' in table])

        elif core.io.exists(file,False):
            cvdict[entry] = core.io.json_read(file)[entry]
            
            if 'experiment_id' in entry:
                # this section updates the sources. We expect this to come afterwards, and therefore this should not throw an exception and should work as expected. 
                cvdict['source_type'] = set(cvdict['source_type']).union(set(component for experiment in cvdict[entry].values() if "required_model_components" in experiment
                       for component in experiment["required_model_components"]))
               
                

            if entry == 'source_id':
                # this section updates the institutions
                cvdict['institution_id'] = {i: institutions[i] for i in sorted({component for source in cvdict[entry].values() for component in source.get("institution_id", [])})}

                # [[i,instutitions[i]] for i in sorted(list(set(component for source in cvdict[entry].values() for component in source.get("institution_id",[]))))]

        elif entry in template:
            cvdict[entry] = template[entry]
        
        else:
            missing.append(entry)


    #  final check 
    diff = set(missing) - set(cvdict)
        
    if diff: 
        raise core.stdout.MissingValueError(f'The following fields are required:{diff} ')

    core.stdout.MissingValueError(f'The following fields are required:{diff} ')


    #  update this to the correct format. 

    cvdict['source_type'] = dict([[s,source_type[s]] for s in cvdict['source_type']])



    core.io.json_write(cvdict, f"{directory}{outloc}/CV.json",sort=True)



    



