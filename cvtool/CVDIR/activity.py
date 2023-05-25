import os
import sys
import glob

try:  # as a module
    from ..core.curses_toolbox import curses, CursesEditor, CursesSelector
    from ..core.stdout import log
    from ..core.io import exists
except:
    # direct usage
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    sys.path.append(parent_dir)

    from core.curses_toolbox import curses, CursesEditor, CursesSelector
    from core.stdout import log, git_user, yymmdd
    from core.io import exists

import json
import argparse
import time
from collections import Counter


print = log(__file__.split("activity")[1])


def main(directory, edit=False):
    if directory[-1] != '/':
        directory += '/'
    exists(directory)

    PROJECT = Counter([i.split('/')[-1].split('_')[0]
                      for i in glob.glob(f'{directory}*.json')]).most_common()[0][0]

    print.info(f"{'Directory Location':50} : {directory:50}")
    print.info(f"{'Project Name:':50} : {PROJECT:50}")

    time.sleep(2)

    data = json.load(open(f'{directory}{PROJECT}_activity_id.json', 'r'))
    # print.warning(data)

    if not edit:
        print.warning('Loading Activity VIEWER. Please Wait')
        time.sleep(2)
        items = data['activity_id']
        editor = CursesSelector(items)
        select = curses.wrapper(editor.main)

        if select == 'new':
            key = input("Enter NEW activity: ")
            value = input("Enter NEW activity description: ")
            if key in data['activity_id']:
                print.error(f'Activity {key} exists')
                sys.exit()
            data['activity_id'][key] = value

    else:

        print.warning('Loading Activity EDITOR. Please Wait')
        time.sleep(2)
        items = data['activity_id']

        def save(pair_list):
            return dict(pair_list)

        editor = CursesEditor(items, save_func=save)
        updates = curses.wrapper(editor.main)

        # print.info(updates)
        import pprint
        pprint.pprint(updates)

    # , save_func=save_items,check = valid)

    # UPDATE THE LAST COMMIT DATA
    git = git_user()
    data['version_metadata']['author'] = f"{git['user']} <{git['email']}>"
    data['version_metadata']['CV_collection_modified'] = yymmdd()
    data['version_metadata']['CV_collection_version'] += '+1 (update on publication)'

    print.warn('version_metadata seems more descriptive than Header')

    # editor = CursesEditor(items, save_func=save_items,check = valid)
    # curses.wrapper(editor.main)


if __name__ == '__main__':

    defaultloc = '/Users/daniel.ellis/WIPwork/CMIP6_CVs'
    edit = True
    # parser = argparse.ArgumentParser(description='Process a directory location.')
    # parser.add_argument('dir_location', type=str, help='Path to the directory')

    # args = parser.parse_args()

    # directory = args.dir_location

    main(defaultloc, edit)
