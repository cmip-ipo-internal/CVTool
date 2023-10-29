import json
import re
import os
import sys
import glob
from collections import Counter
from typing import Any, Dict

try:
    from ..core.stdout import log
    from ..core.io import exists
except:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    sys.path.append(parent_dir)
    from core.stdout import log
    from core.io import exists

from pprint import pprint

print = log(__file__.split('cvtool')[1])

path2ini = lambda s: s.replace('<', '%(').replace('>', ')s').replace('activity_id', 'activity_drs')

def loopformat(dictionary: Dict[str, Any], key: str, prefix: str) -> str:
    try:
        for dkey, value in dictionary.items():
            prefix += f"{dkey.ljust(30)} | {value.get(key)}\n"
    except AttributeError:
        for dkey, value in dictionary.items():
            prefix += f"{dkey.ljust(30)} | {value}\n"
    return prefix

def make(output_loc, CVDIR=None, CVFILE=None, INI_CATEGORIES=''):
    exists(output_loc)

    if CVDIR[-1] != '/':
        CVDIR += '/'

    if bool(CVDIR) & bool(CVFILE):
        print.warning('Both a CV file and a CV Directory defined. Using CVDIR only!')

    if exists(CVDIR):
        PROJECT = Counter([i.split('/')[-1].split('_')[0] for i in glob.glob(f'{CVDIR}*.json')]).most_common()[0][0]

        def read_section(section: str) -> Dict[str, Any]:
            return json.load(open(exists(f'{CVDIR}{PROJECT}_{section}.json'), 'r'))
    else:
        exists(CVFILE)
        CVOBJ = json.load(open(f'{CVFILE}.json', 'r'))
        PROJECT = re.search('/(\w+)_CV.json', CVLOC)[1]

        def read_section(section: str) -> Dict[str, Any]:
            return CVOBJ[section]

    if not INI_CATEGORIES:
        INI_CATEGORIES = __file__.replace('cv2ini.py', '') + '../sampleconf/ini_categories.json'
        print.warn('Reading INI categories from preset file. Please ensure these are correct.')

    DRS = read_section('DRS').get('DRS')

    cat = json.load(open(INI_CATEGORIES, 'r'))
    counter = 0
    categories = ''
    for requirement in ('required', 'optional'):
        req = requirement == 'required'
        for row in cat[requirement]:
            if row.get('name') != 'description':
                index = counter
                counter += 1
            else:
                index = 99
            categories += f"{row.get('name'):20} | {row.get('data_type'):6} | {bool(req):5} | {bool(row.get('supported')):5} | {index}\n"

    category_defaults = '    project | ' + PROJECT
    filename_format = path2ini(DRS.get("filename_template"))
    dataset_id = path2ini(DRS.get("directory_path_template"))
    directory_format = f'%(root)s/{dataset_id}/%(version)s'
    dataset_name_format = f"mip_era=%(mip_era)s, source_id=%(source_id)s, experiment=%(experiment_title)s, member_id=%(member_id)s, variable=%(variable_id)s, version=%(version)s"

    mip_era_options = read_section('mip_era')
    activity_drs_options = ', '.join(list(read_section('activity_id').keys()))
    institution_id_options = ', '.join(list(read_section('institution_id').keys()))
    source_id_options = ', '.join(list(read_section('source_id').keys()))
    experiment_id_options = ', '.join(list(read_section('experiment_id').keys()))

    maps = 'experiment_title_map, model_cohort_map, las_time_delta_map'
    experiment_title_map = loopformat(read_section('experiment_id'), 'experiment', 'map(experiment_id : experiment_title)\n')
    member_id_pattern = f'[%(sub_experiment_id)s-]%(variant_label)s'
    table_id_options = ', '.join(list(read_section('table_id')))
    variable_id_pattern = f'%(string)s'
    grid_label_options = ', '.join(list(read_section('grid_label').keys()))
    model_cohort_map = loopformat(read_section('source_id'), 'cohort', 'map(source_id : model_cohort)\n')
    project_options = PROJECT
    sub_experiment_id_options = ', '.join(list(read_section('sub_experiment_id').keys()))
    variant_label_pattern = f'r%(digit)si%(digit)sp%(digit)s'
    frequency_options = ', '.join(list(read_section('frequency').keys()))
    version_pattern = f'v%(digit)s'
    las_time_delta_map = loopformat(read_section('frequency'), False, 'map(frequency : las_time_delta)\n')

    print.warning('Handler CMOR CF Version definitions required. Do we want an ESGFparse file?')
    handler = 'esgcet.config.cmip6_handler:CMIP6Handler'
    min_cmor_version = '3.2.4'
    min_cf_version = '1.6'
    min_data_specs_version = '01.00.13'
    create_cim = 'true'
    source_type_delimiter = 'space'
    activity_id_delimiter = 'space'
    realm_delimiter = 'space'
    model_cohort_delimiter = 'space'
    las_configure = 'false'
    extract_global_attrs = 'WE HAVE NOT YET EXTRACTED THESE'
    thredds_exclude_variables = 'CHECK WHERE TO FIND THESE'
    variable_locate = 'ASK ABOUT THIS'
    variable_per_file = 'true'
    version_by_date = 'true'

    write = ('categories', 'category_defaults', 'filename_format', 'dataset_id', 'directory_format', 'dataset_name_format', 'mip_era_options', 'activity_drs_options', 'institution_id_options', 'source_id_options', 'experiment_id_options', 'maps', 'experiment_title_map', 'member_id_pattern', 'table_id_options', 'variable_id_pattern', 'grid_label_options', 'model_cohort_map', 'project_options', 'sub_experiment_id_options', 'variant_label_pattern', 'frequency_options', 'version_pattern', 'las_time_delta_map', 'handler', 'min_cmor_version', 'min_cf_version', 'min_data_specs_version', 'create_cim', 'source_type_delimiter', 'activity_id_delimiter', 'realm_delimiter', 'model_cohort_delimiter', 'las_configure', 'extract_global_attrs', 'thredds_exclude_variables', 'variable_locate', 'variable_per_file', 'version_by_date')

    with open(f"{output_loc}{PROJECT}.ini", 'w') as f:
        for var in write:
            f.write(f"{var} = {locals().get(var)}\n\n")

if __name__ == '__main__':
    CVDIR = "/Users/daniel.ellis/W
