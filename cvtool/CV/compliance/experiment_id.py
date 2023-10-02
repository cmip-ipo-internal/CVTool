import json
from jsonschema import validate

# Define your JSON schema
schema = {
    "type": "object",
    "properties": {
        "activity_id": {"type": "array", "items": {"type": "string"}},
        "additional_allowed_model_components": {"type": "array", "items": {"type": "string"}},
        "experiment": {"type": "string"},
        "experiment_id": {"type": "string"},
        "parent_activity_id": {"type": "array", "items": {"type": "string"}},
        "parent_experiment_id": {"type": "array", "items": {"type": "string"}},
        "required_model_components": {"type": "array", "items": {"type": "string"}},
        "sub_experiment_id": {"type": "array", "items": {"type": "string"}},
        "description": {"type": "string"},
        "tier": {"type": "integer"},
        "start": {"type": "integer"},
        "end": {"type": "integer"}
    },
    "required": ["activity_id", "additional_allowed_model_components", "experiment", "experiment_id", 
                 "parent_activity_id", "parent_experiment_id", "required_model_components", 
                 "sub_experiment_id", "description", "tier", "start", "end"]
}


 
def check(key, compareset, experiment):
    if set(experiment.get(key)) - compareset:
        raise AssertionError(f"\n\nMissing value: {set(experiment.get(key)) - compareset} \n\n in column '{key}' \n\n for {experiment}")
        



def test(CV):


    source_type = set(CV.get('source_type'))
    activity_id = set(CV.get('activity_id')).union(set(['no parent']))

    for name, experiment in CV.get('experiment_id').items():

        # schema test
        try:
            # Validate the JSON data against the schema
            validate(instance=experiment, schema=schema)
            print("Validation successful.")
        except Exception as e:
            print(f"Validation failed: {e}")

        # model types 
        check("additional_allowed_model_components", source_type,experiment)

        # activity
        check("activity_id",activity_id,experiment)
        check("parent_activity_id",activity_id,experiment)
        
        # id 
        assert name == experiment.get('experiment_id')
        


if __name__ == '__main__':
    CV = json.load(open('/Users/daniel.ellis/WIPwork/CVTool/mip_specific/lesf/testdirLESF/cv_cmor/CMIP6Plus_CV.json')).get('CV')
    test(CV)