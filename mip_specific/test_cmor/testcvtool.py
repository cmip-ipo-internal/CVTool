from __future__ import print_function
import cmor,os

table_path = '/var/folders/hc/s_7lggq12nndglbdyrn3f91m1l58yd/T/cvtool.miptables.f9gwh6gn/mip_cmor_tables/out/'

input_path = "/Users/daniel.ellis/WIPwork/CVTool/mip_specific/lesf/testdirLESF/cv_cmor/CMIP6Plus_input.json" 

cv_path = input_path.replace('_input','_CV')


newinput = f'{table_path}testcvtool.json'
newCV = f'{table_path}testCVfile.json'

os.system(f'cp {cv_path} {newCV}')

relative_in_path = os.path.relpath(newinput, table_path)

relative_cv_path = os.path.relpath(newCV, table_path)



# update cv file with location
import json
import os

# Read the JSON file
with open(input_path, "r") as json_file:
    data = json.load(json_file)

# Modify the desired item
data["_controlled_vocabulary_file"] = relative_cv_path

# Write the modified data to the output file
with open(newinput, "w") as output_file:
    json.dump(data, output_file, indent=4)



def multi_call_test():
    cmor.setup(inpath=table_path,
               
            #    '/Users/daniel.ellis/WIPwork/cmor/TestTables'
            netcdf_file_action=cmor.CMOR_REPLACE)

    cmor.dataset_json(relative_in_path)
    table = 'CMIP6Plus_APmon.json'
    # no amon in cmip6plus
    cmor.load_table(table)
    axes = [{'table_entry': 'time',
             'units': 'days since 2000-01-01 00:00:00',
             },
            {'table_entry': 'latitude',
             'units': 'degrees_north',
             'coord_vals': [0],
             'cell_bounds': [-1, 1]},
            {'table_entry': 'longitude',
             'units': 'degrees_east',
             'coord_vals': [90],
             'cell_bounds': [89, 91]},
            ]

    axis_ids = list()
    for axis in axes:
        axis_id = cmor.axis(**axis)
        axis_ids.append(axis_id)
    varid = cmor.variable('ts', 'K', axis_ids)
    cmor.write(varid, [275], time_vals=[15], time_bnds=[[0, 30]])
    print('First write worked as expected')
    try:
        cmor.write(varid, [275], time_vals=[15], time_bnds=[[0], [30]])
        raise Exception("We shouldn't be getting in here")
    except BaseException:
        print('Second write that should have failed did fail, good!')
        pass
    cmor.close(varid)
    print('Success')


if __name__ == '__main__':
    multi_call_test()

