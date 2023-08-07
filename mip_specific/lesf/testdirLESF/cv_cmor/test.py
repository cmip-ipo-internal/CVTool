import cmor
import numpy as np

# Code used to quickly test input.json

error_flag = cmor.setup(inpath='.', netcdf_file_action=cmor.CMOR_REPLACE)

#error_flag = cmor.dataset_json("my_input.json")
error_flag = cmor.dataset_json("CMIP6Plus_input.json")

cmor.load_table("CMIP6Plus_APmon.json")

time = cmor.axis(table_entry="time", units="days since 2000-01-01",
                         coord_vals=np.array([30.0, 60.0]),
                         cell_bounds=np.array([15.0, 45.0, 75.0]))
height2m = cmor.axis(table_entry="height2m", units="m", coord_vals=np.array((2.0,)))
latitude = cmor.axis(table_entry="latitude", units="degrees_north",
                        coord_vals=np.array(range(5)),
                        cell_bounds=np.array(range(6)))
longitude = cmor.axis(table_entry="longitude", units="degrees_east",
                        coord_vals=np.array(range(5)),
                        cell_bounds=np.array(range(6)))
axis_ids = [longitude, latitude, time,height2m]
tas_var_id = cmor.variable(table_entry="tas", axis_ids=axis_ids, units="K")
data = np.random.random(50) + 300
reshaped_data = data.reshape((5, 5, 2, 1))





cmor.write(tas_var_id, reshaped_data)

cmor.close()
