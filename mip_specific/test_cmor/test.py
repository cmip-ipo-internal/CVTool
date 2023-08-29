from __future__ import print_function
import cmor


def multi_call_test():
    cmor.setup(inpath='/var/folders/hc/s_7lggq12nndglbdyrn3f91m1l58yd/T/cmortool.miptables.0jtrqwl_/mip_cmor_tables/out'
            #    '/Users/daniel.ellis/WIPwork/cmor/TestTables'
               , netcdf_file_action=cmor.CMOR_REPLACE)

    cmor.dataset_json("./CMOR_input_example.json")
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

