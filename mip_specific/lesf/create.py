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
        experiments[row.get(Name)] = get_experiment(row)



def experiment(edata,optional):
    
    return  {
      "activity_id": [
        optional.get('activity_id')
      ],
      "additional_allowed_model_components": [
        # "AER",
        # "CHEM",
        # "BGC"
      ],
      "description": edata.get('Description'),
      "end_year": edata.get('End Year'),
      "experiment": "1 percent per year increase in CO2",
      
      "experiment_id": "1pctCO2",
      "min_number_yrs_per_sim": "150",
      "parent_activity_id": [
        optional.get('activity_id')
      ],
      "parent_experiment_id": [
        # "piControl"
      ],
      "required_model_components": [
        # "AOGCM"
      ],
      "start_year": edata.get('Start Year'),
      "sub_experiment_id": [
      ],
      "tier": edata.get('Tier')
    }
