import os
import sys
import glob

try:  # as a module
    from .experiment_vars import experiment_template
    from . import experiment_checks as exchk
    from ..core.curses_toolbox import curses, CursesEditor, CursesSelector
    from ..core.stdout import log
    from ..core.io import exists
except:
    # direct usage
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    sys.path.append(parent_dir)

    from experiment_vars import experiment_template
    import experiment_checks as exchk
    from core.curses_toolbox import curses, CursesEditor, CursesSelector
    from core.stdout import log, git_user, yymmdd
    from core.io import exists

import json
import argparse
import time
from pprint import pprint
from collections import Counter


print = log(__file__.split("experiment")[1])



def update_meta(data):
    """
    Update metadata information in the data dictionary.

    Args:
        data (dict): The data dictionary to update.

    Returns:
        None

    """
    git = git_user()
    data['version_metadata']['author'] = f"{git['user']} <{git['email']}>"
    data['version_metadata']['CV_collection_modified'] = yymmdd()
    data['version_metadata']['CV_collection_version'] += '+1 (update on publication)'

    print.warning('version_metadata seems more descriptive than Header')



def main(directory,selected_experiment=None):
    if directory[-1] != '/':
        directory += '/'
    exists(directory)

    PROJECT = Counter([i.split('/')[-1].split('_')[0]
                      for i in glob.glob(f'{directory}*.json')]).most_common()[0][0]

    print.info(f"{'Directory Location':50} : {directory:50}")
    print.info(f"{'Project Name:':50} : {PROJECT:50}")

    time.sleep(2)
    PATH=f'{directory}{PROJECT}'
    data = json.load(open(f'{PATH}_experiment_id.json', 'r'))
    # print.warning(data)

    eid = data['experiment_id'].copy()


    if not selected_experiment :

        time.sleep(2)
        items = list(eid.keys())

        editor = CursesSelector(items,title='Select experiment to edit')
        selected_experiment = curses.wrapper(editor.main)[1]


        pprint( eid[selected_experiment])
    else:
        assert selected_experiment in eid

    ''' 
    Start the editor
    '''
    
    items = eid[selected_experiment]

    def save(pair_list):
        return dict(pair_list)
    
    def check(key,value):
        if hasattr(exchk, key):
            return getattr(exchk, key)(PATH,value)
        else: 
            return True

    editor = CursesEditor(items, save_func=save, check=check, title='EDIT an Experiment') 
    update = curses.wrapper(editor.main)



        # if select == 'new':
        #     data = new_activity(data)

    # else:

    #     print.warning('Loading Activity EDITOR. Please Wait')
    #     time.sleep(2)
    #     items = data['activity_id']

    #     def save(pair_list):
    #         return dict(pair_list)

    #     editor = CursesEditor(items, save_func=save)
    #     updates = curses.wrapper(editor.main)

    #     # print.info(updates)
    #     import pprint
    #     pprint.pprint(updates)
    #     # update the table 
        


    # # UPDATE THE LAST COMMIT DATA
    # data = update_meta(data)

    





if __name__ == '__main__':

    defaultloc = '/Users/daniel.ellis/WIPwork/CMIP6_CVs'

    # parser = argparse.ArgumentParser(description='Process a directory location.')
    # parser.add_argument('dir_location', type=str, help='Path to the directory')

    # args = parser.parse_args()

    # directory = args.dir_location

    main(defaultloc)
