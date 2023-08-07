loc  = '/Users/daniel.ellis/WIPwork/mip-cmor-tables/Tables/'

import cmor 
cmor.setup(
    inpath=loc,
    netcdf_file_action=cmor.CMOR_REPLACE_4,
    set_verbosity=cmor.CMOR_NORMAL
)
import os 
inputfile = os.path.abspath('testdirLESF/cv_cmor/CMIP6Plus_input.json')
print(inputfile)
cmor.dataset_json(inputfile)