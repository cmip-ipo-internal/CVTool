import json
import re
import glob
from collections import Counter
from ..core.stdout import log
from ..core.io import exists
from pprint import pprint

print = log(__file__.split('cvtool')[1])


# use argparse
INI_CATEGORIES = ''

'''
#  only need CV DIR or CVFILE
If both specified, then the CVDIR is selected.
Combination can be used to run tests for equivalency.
'''
CVDIR = "/Users/daniel.ellis/WIPwork/CMIP6_CVs"
# OR
CVFILE = "/Users/daniel.ellis/WIPwork/mip-cmor-tables/mip_cmor_tables/out/CMIP6Plus_CV.json"


''' functions '''

if CVDIR[-1] != '/': CVDIR += '/'


if bool(CVDIR) & bool(CVFILE): print.warning(
    'Both a CV file and a CV Directory defined. Using CVDIR only!')

if CVDIR:
    exists(CVDIR)
    PROJECT = Counter([i.split('/')[-1].split('_')[0] for i in glob.glob(f'{CVDIR}*.json')]).most_common()[0][0]
    read_section = lambda section: json.load(
        open(exists(f'{CVDIR}{PROJECT}_{section}.json'), 'r'))[section]

else:
    exists(CVFILE)
    CVOBJ = json.load(open(f'{CVFILE}.json', 'r'))
    PROJECT = re.search('/(\w+)_CV.json', CVLOC)[1]
    read_section = lambda section: CVOBJ[section]


path2ini = lambda s: s.replace('<', '%(').replace('>', ')s').replace('activity_id','activity_drs')

def loopformat (dictionary,key,prefix):
    try:
        for dkey, value in dictionary.items():
            prefix += f"{dkey.ljust(30)} | {value.get(key)}\n"
    except AttributeError:
        for dkey, value in dictionary.items():
            prefix += f"{dkey.ljust(30)} | {value}\n"

    return prefix


'''
Read Files
Do this here such that we crash if missing, and not after computation

'''
# check if exists too


if not INI_CATEGORIES:
    INI_CATEGORIES = __file__.replace(
        'cv2ini.py', '')+'../sampleconf/ini_categories.json'


DRS = read_section('DRS')


# Categories

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


#  Filenames

filename_format = path2ini(DRS.get("filename_template"))

dataset_id = path2ini(DRS.get("directory_path_template"))

directory_format = f'%(root)s/{dataset_id}/%(version)s'

dataset_name_format = f"mip_era=%(mip_era)s, source_id=%(source_id)s, experiment=%(experiment_title)s, member_id=%(member_id)s, variable=%(variable_id)s, version=%(version)s"

# ids
print.warning('Manually added CMIP6 Plus mipera file to CMIP6 dir')
mip_era_options = read_section('mip_era')

activity_drs_options = ', '.join(list(read_section('activity_id').keys()))

institution_id_options = ', '.join(list(read_section('institution_id').keys()))

source_id_options = ', '.join(list(read_section('source_id').keys()))

experiment_id_options = ', '.join(list(read_section('experiment_id').keys()))

# maps

maps = 'experiment_title_map, model_cohort_map, las_time_delta_map'

experiment_title_map = loopformat(read_section('experiment_id'),'experiment','map(experiment_id : experiment_title)\n')


member_id_pattern = f'[%(sub_experiment_id)s-]%(variant_label)s'

table_id_options = ', '.join(list(read_section('table_id')))

variable_id_pattern = f'%(string)s'

grid_label_options = ', '.join(list(read_section('grid_label').keys()))

model_cohort_map = loopformat(read_section('source_id'),'cohort','map(source_id : model_cohort)\n')

project_options = PROJECT

sub_experiment_id_options =  ', '.join(list(read_section('sub_experiment_id').keys()))

variant_label_pattern = f'r%(digit)si%(digit)sp%(digit)sf%(digit)s'

frequency_options = ', '.join(list(read_section('frequency').keys()))

version_pattern = f'v%(digit)s'

las_time_delta_map = loopformat(read_section('frequency'),False,'map(frequency : las_time_delta)\n') 
########
print.warning('Handler CMOR CF Version definitions required. Do we want a ESGFparse file?')
########
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

# extract_global_attrs = frequency, realm, product, nominal_resolution, source_type, grid, creation_date, variant_label, sub_experiment_id, further_info_url, activity_id, data_specs_version


# thredds_exclude_variables = a, a_bnds, alev1, alevel, alevhalf, alt40, b, b_bnds, bnds, bounds_lat, bounds_lon, dbze, depth, depth0m, depth100m, depth_bnds, geo_region, height, height10m, height2m, lat, lat_bnds, latitude, latitude_bnds, layer, lev, lev_bnds, location, lon, lon_bnds, longitude, longitude_bnds, olayer100m, olevel, oline, p0, p220, p500, p560, p700, p840, plev, plev3, plev7, plev8, plev_bnds, plevs, pressure1, region, rho, scatratio, sdepth, sdepth1, sza5, time, time1, time2, time_bnds, vegtype, i, j, rlat, rlat_bnds, sector, type, vertices_latitude, vertices_longitude

# variable_locate = ps, ps_ | tau, tau_

variable_per_file = 'true'

version_by_date = 'true'

