''' 
A run template for self.CMOR for use with the 
'''
from .. import core
# import cmor

class CMORise:
    def __init__(self, tables, cmor_input, verbose=False):
        # verbose can also be NORMAL
        import cmor as cmor_main
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
        self.cmor.load_table(table_id)

    def process_data(self):
        """
        Process data according to self.CMOR table and dimensions.
        """
        input_dict = core.io.json_read(self.cmor_input)
        cvfile = core.io.json_read(input_dict["_controlled_vocabulary_file"])
        tables = cvfile['CV']['table_id']
        table = tables[2]

        self.load_table(table + '.json')

        print('only testing the first table', table)

        coord_dict = core.io.json_read(input_dict["_AXIS_ENTRY_FILE"])["axis_entry"]
        table_dict = core.io.json_read(f'{self.tables}{table}.json')
        vars = table_dict['variable_entry']

        data = []
        axis = []

        for v in vars:
            dimensions = vars[v]['dimensions']

            # Create a list of dimensions to iterate over
            if isinstance(dimensions, str):
                dimensions = dimensions.split(' ')

            for dim in dimensions:
                # previous table files had these as a str, so needed .split()
                print('-', dim, type(vars[v]['dimensions']), '-')

                d = coord_dict[dim]

                if 'time' in dim:
                    ax = dict(table_entry=dim, units='days since 2000-01-01 00:00:00')
                    print(ax)
                    axis_id = self.cmor.axis(**ax)
                    axis.append(axis_id)
                    data.append(1.)
                else:
                    try:
                        bounds = [float(d['valid_min']), float(d['valid_max'])]
                        data.append(sum(bounds) / 2.)
                        ax = dict(table_entry=dim, units=d['units'], cell_bounds=bounds, coord_vals=[sum(bounds) / 2.])
                        print(ax)
                        axis_id = self.cmor.axis(**ax)
                        axis.append(axis_id)
                    except Exception as e:
                        print(e)
                        # Handle the exception as needed

            ivar = self.cmor.variable(v, units=vars[v]['units'], axis_ids=axis)
            self.cmor.write(ivar, data)
            print(axis, data, vars[v]['units'])

        self.cmor.close()


# if __name__ == "__main__":
#     tables = 'path/to/tables/'
#     cmor_input = 'path/to/dataset.json'
#     table = 'table_name.json'

#     converter = self.CMORise(tables, cmor_input, table)
#     converter.run_conversion()
