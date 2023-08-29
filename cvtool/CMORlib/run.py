''' 
A run template for self.CMOR for use with the 
'''
from .. import core
import numpy as np
# import cmor

class CMORise:
    def __init__(self, tables, cmor_input, verbose=False):
        # verbose can also be NORMAL
        try:
            import cmor as cmor_main
        except ModuleNotFoundError:
            raise ModuleNotFoundError('We are unable to find the "cmor" library in python. Please check this has been installed and you are using the correct environment')
        self.cmor = cmor_main
        self.tables = tables
        self.cmor_input = cmor_input
        self.verbose = verbose

        print(tables)
        # lets initialize the self.CMOR
        self.setup_cmor()
        self.load_cv()

    def setup_cmor(self):
        """
        Set up self.CMOR with the provided parameters.
        """
        if self.verbose:
            verb = self.cmor.CMOR_NORMAL
        else:
            verb = self.cmor.CMOR_QUIET

        self.cmor.setup(
            inpath=self.tables,
            netcdf_file_action=self.cmor.CMOR_REPLACE_4,
            set_verbosity=verb
        )

    def load_cv(self):
        """
        Load the dataset JSON file.
        """
        self.cmor.dataset_json(self.cmor_input)

    def load_table(self, table_id):
        """
        Load the self.CMOR table.
        """
        print(table_id)
        self.cmor.load_table(table_id)

    def process_data(self):
        """
        Process data according to self.CMOR table and dimensions.
        """
        input_dict = core.io.json_read(self.cmor_input)
        cvfile = core.io.json_read(input_dict["_controlled_vocabulary_file"])
        mipera = cvfile['CV'].get('mip_era','')+'_'
         
        tables = cvfile['CV']['table_id']
        table =  tables[0] 
        # in test case table is apmon as this is the only one suplied. 
        # table = 'CMIP6_APmon'

        #  APMON IS EVIL - not in cmip 6 and resembles AMON


        print('TEST ONE OPTION - SUPPLY TABLE PREFIX')

        print(tables)
        self.load_table(f'{mipera}{table}.json')

        print('only testing the first table',mipera, table)

        coord_dict = core.io.json_read(f"{self.tables}{input_dict['_AXIS_ENTRY_FILE']}")["axis_entry"]
        table_dict = core.io.json_read(f'{self.tables}{table}.json')
        vars = table_dict['variable_entry']

        data = []
        axis = []

        for v in vars:
            dimensions = vars[v]['dimensions']

            # Create a list of dimensions to iterate over
            if isinstance(dimensions, str):
                dimensions = dimensions.split(' ')
            shape = []
            axis = []
            awkward_dims = ['plev', 'tau', 'sza5', 'alt40', 'dbze']
            if any([d in str(dimensions) for d in awkward_dims]):
                    continue
            for dim in dimensions:
                # previous table files had these as a str, so needed .split()
                print('-', dim, type(vars[v]['dimensions']), '-')

                d = coord_dict[dim]

                if 'time' in dim:
                    ax = dict(table_entry=dim, units='days since 2000-01-01 00:00:00', 
                              coord_vals=[30,60], cell_bounds=[15,45,75])
                    print(ax)
                    axis_id = self.cmor.axis(**ax)
                    axis.append(axis_id)
                    shape.append(2)
                else:
                    try:
                        try:
                            bounds = [float(d['valid_min']), float(d['valid_max'])]
                        except:
                            bounds = [0, 1]
                        ax = dict(table_entry=dim, units=d['units'], cell_bounds=bounds, coord_vals=[sum(bounds) / 2.])
                        print(ax)
                        axis_id = self.cmor.axis(**ax)
                        axis.append(axis_id)
                        shape.append(1)
                    except Exception as e:
                        print(e)
                        # Handle the exception as needed

            ivar = self.cmor.variable(v, units=vars[v]['units'], axis_ids=axis, positive=vars[v]['positive'])
            data = np.random.random(shape) 
            if vars[v]['ok_min_mean_abs'] !="":
                min_v = float(vars[v]['ok_min_mean_abs'])
                max_v = float(vars[v]['ok_max_mean_abs'])
                data = min_v + (max_v - min_v) * data
            self.cmor.write(ivar, data)
            # close each file as you go
            self.cmor.close(ivar)
            print(axis, data, vars[v]['units'])

        #self.cmor.close()


# if __name__ == "__main__":
#     tables = 'path/to/tables/'
#     cmor_input = 'path/to/dataset.json'
#     table = 'table_name.json'

#     converter = self.CMORise(tables, cmor_input, table)
#     converter.run_conversion()
