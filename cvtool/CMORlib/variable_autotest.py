import cmor
import numpy as np


def lmap(f, x):
    """
    Apply function `f` to each element of iterable `x` and return the results as a list.

    Parameters:
    f (callable): A function to be applied to each element.
    x (iterable): An iterable containing elements to be processed.

    Returns:
    list: A list containing the results of applying function `f` to each element of `x`.
    """
    return list(map(f, x))


def main(dataset_in,table):
    cmor.setup(
        inpath = baseLocation, #'Tables',  
        netcdf_file_action = cmor.CMOR_REPLACE_4,
        set_verbosity=       cmor.CMOR_QUIET
    )

    cmor.dataset_json(dataset_in)    
    cmor.load_table(table)

    inputDict= json.load(open(dataset_in))
    coordDict = json.load(open(inputDict["_AXIS_ENTRY_FILE"]))["axis_entry"]
    tableDict = json.load(open(f'{baseLocation}{table}'))
    vars = tableDict['variable_entry']

    data = []
    axis = []

    for dims in vars[v]['dimensions'].split():
        print('-', dims, '-')
        d = coordDict[dims]

        if 'time' in dims:
            ax = dict(table_entry=dims, units='days since 2000-01-01 00:00:00')
            print(ax)
            axis_id = cmor.axis(**ax)
            axis.append(axis_id)
            data.append(1.)
        else:
            try:
                bounds = [float(d['valid_min']), float(d['valid_max'])]
                data.append(sum(bounds) / 2.)
                ax = dict(table_entry=dims, units=d['units'], cell_bounds=bounds, coord_vals=[sum(bounds) / 2.])
                print(ax)
                axis_id = cmor.axis(**ax)
                axis.append(axis_id)
            except Exception as e:
                print(e)
                ...

    ivar = cmor.variable(v, units=vars[v]['units'], axis_ids=axis)
    
    cmor.write(ivar, data)
    axis,data,vars[v]['units']

    cmor.close()



if __name__ == '__main__':

    import argparse

    defaults = {
        'MIPname': 'input4MIPs',
        'baseLocation': '../Tables/',
        'writeLocation': './InputFiles/',
        'sourceId': 'CCSM4-rcp26-1-0',
        'activityId': 'input4MIPs',
        'region': 'antarctica',
        'experimentId': 'testingtestingtesting'
    }

    parser = argparse.ArgumentParser()
    parser.add_argument('--MIPname', default=defaults['MIPname'], help='MIP name')
    parser.add_argument('--baseLocation', default=defaults['baseLocation'], help='Base location')
    parser.add_argument('--writeLocation', default=defaults['writeLocation'], help='Write location')
    parser.add_argument('--sourceId', default=defaults['sourceId'], help='Source ID')
    parser.add_argument('--activityId', default=defaults['activityId'], help='Activity ID')
    parser.add_argument('--region', default=defaults['region'], help='Region')
    parser.add_argument('--experimentId', default=defaults['experimentId'], help='Experiment ID')
    args = parser.parse_args()

    MIPname = args.MIPname
    baseLocation = args.baseLocation
    writeLocation = args.writeLocation
    sourceId = args.sourceId
    activityId = args.activityId
    region = args.region
    experimentId = args.experimentId

    table = f"{MIPname}_Omon.json"




    # I create a new input file for testing/ 
    from new_Input import create
    newinput = create(MIPname,sourceId,experimentId,activityId, region, baseLocation,writeLocation)


    main(newinput,table)

