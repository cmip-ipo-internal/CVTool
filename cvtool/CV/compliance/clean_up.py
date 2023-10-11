''' 

Lets add some checks to ensure that we do not have 

This is a reverse checks selection. The creation of the CVS ensures we do not have missing data. 

The cleanup removes any items which are not used within the CV - hopefully making it easier to see the difference between CV collections. 

'''


def prune(CV): 
    
    activity_id = []
    source_type = []
    sub_experiment_id = []
    
    for _,experiment in CV.get('experiment_id',{}).items():
        for a in ['activity_id','parent_activity_id']:
            activity_id.extend(experiment.get(a,[]))

        source_type.extend(experiment.get('additional_allowed_model_source_type',[]))

        source_type.extend(experiment.get('required_model_source_type',[]))

        sub_experiment_id.extend(experiment.get('"sub_experiment_id"',[]))


    institution_id = []
    for _,source in CV.get('source_id',{}).items():

        institution_id.extend(source.get("institution_id",[]))

    keys = ['activity_id','source_type','sub_experiment_id','institution_id']

    lc = locals()
    for keystr in keys:
        keyval = set(lc[keystr])
        CV[keystr] = {key: value for key, value in CV[keystr].items() if key in keyval}

    return CV
        
        



    


        

    













