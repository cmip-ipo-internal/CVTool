import sys
sys.path.append('../../')
# from mymodule import myfunction


import cvtool
from cvtool import CV



prefix = 'MY_PREFIX'


# Example usage
handler = CV.CVDIR(prefix=prefix, directory='testdir', base_files=[
    "mip_era",
    # "experimet_id",
    # "table_id"
])

# # Update all files with data using the example update function

data = {'mip_era':{'create':{'mipera':prefix,'institution':'testipo'},'update':{'updatedadd':'topleveltest'}}}


handler.update_all(data)






def lesf_parse():


    import pandas as pd
    df = pd.read_csv('./data/exp_in.csv')

    optional = {'activity_id':'LESF'}

    experiments = {}
    for i,row in df.iterrows():
        experiments[row.get('Name')] = get_experiment(row)



def get_experiment(edata,optional):
    
    return  {
      "activity_id": [
        optional.get('activity_id')
      ],
      "additional_allowed_model_components": [
        # "AER",
        # "CHEM",
        # "BGC"

        # existing cvs:most experiments require - either AGCM(atmos) AOGCM(coupled)
        # BGC biogeochem (additional to mips. looking at specific models etc. 
        #)
        # copy from existing - taking DAMIP -> reqired and allowed are the same . 
        # in the source_type/? json file. 

      ],
      "description": edata.get('Description'),
      "end_year": edata.get('End Year'),
      "experiment": "1 percent per year increase in CO2",

      "experiment_id": edata.get('Name'),
      "min_number_yrs_per_sim": "150",
      "parent_activity_id": [
        optional.get('activity_id')
      ],
      "parent_experiment_id": [
        # "piControl"

        # existing experiemtns and new hist are all children of the PI control. 

        # future experiments - a continuation of historical 
        # e.g. futureghg has parent hist ghg



      ],
      "required_model_components": [
        # "AOGCM"

        # 

      ],
      "start_year": edata.get('Start Year'),
      "sub_experiment_id": [
          
        #    *currently - list as 'none'
        #  if repeated at a lalter point with different/updated forcing this can be used to distinguish these. 
      ],
      "tier": edata.get('Tier')
    }



# CMOR 
#  produce amon taz for a range of the experiments. (a representatice variable

# apmontas

# check that this works with an older version of CMOR? not versions. 
# MM 3.7.1

# Set of tables - Put them on Jasmin. 
# System that wraps around CMOR... 


# activity id - cmip lesfmip
# the rest shoudl remain mainly the same . 

# grid the same
#  list of tables is in the CVS file 


#  generic CV needs to be kept consistant with table_id
#  might potentially break this down into single file field - in the same format as the CVS repo 
# /Users/daniel.ellis/WIPwork/mip-cmor-tables/Tables/generic_CV.json 

# esm- => emission driven versions 


















'''
sub experiement id 
 lesef mip future 
  
 subexp  start daate
 dcpp start date- run forwards, differet start = run forwards . 


 cmip , prublish as amip in subespeirment 
 seriesmp-r1-p1-f1

 make it work for cmor 

providence entry in the experiemtn - e.g. cmip 6 cmip ... historically x and y 

input 4 mips 

 

 only takes the 5 experimetns from CMIP 6 by DAMIP and own them. and adds the extra 7 experiment s

'''