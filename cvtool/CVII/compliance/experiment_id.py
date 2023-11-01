import json
from jsonschema import validate

# Define your JSON schema


def schema_gen(activities, source_type):

    return {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {
            "experiment_id": {"type": "string"},
            "activity_id": {
                "type": "array",
                "items": {
                   "type": "string",
                   "enum": activities
                },
                "minItems": 1
            },
            "experiment": {"type": "string"},
            "description": {"type": "string"},
            "start": {
                "anyOf": [
                    {"type": "integer", "minimum": 1700},
                    {"enum": ["none"]}
                ]
            },
            "end": {
                "anyOf": [
                    {"type": "integer", "maximum": 2100},
                    {"enum": ["none"]}
                ]
            },
            "sub_experiment_id": {
                "type": "array",
                "items": {"type": "string"},
                "minItems": 1
            },
            "parent_activity_id": {
                "type": "array",
                "items": {
                    "type": "string",
                    "enum": activities
                },
                "minItems": 1
            },
            "parent_experiment_id": {
                "type": "array",
                "items": {"type": "string"},
                "minItems": 1
            },
            "required_model_components": {
                "type": "array",
                "items": {"type": "string"},
                "minItems": 1
            },
            "additional_allowed_model_components": {
                "type": "array",
                "items": {
                    "type": "string",
                          "enum": source_type
                          },
                "minItems": 0
            },
            "tier": {
                "type": "integer",
                "enum": [1, 2, 3]
            }
        },
        "required": ["experiment_id", "activity_id", "experiment", "description", "start", "end", "sub_experiment_id", "parent_activity_id", "parent_experiment_id", "required_model_components", "additional_allowed_model_components", "tier"],
        "additionalProperties": False
    }


def check(key, compareset, experiment):
    if set(experiment.get(key)) - compareset:
        raise AssertionError(
            f"\n\nMissing value: {set(experiment.get(key)) - compareset} \n\n in column '{key}' \n\n for {experiment}")


def test(CV):

    source_type = set(CV.get('source_type'))
    activity_id = set(CV.get('activity_id')).union(set(['no parent']))

    for name, experiment in CV.get('experiment_id').items():

        # schema test
        try:
            # Validate the JSON data against the schema
            validate(instance=experiment, schema=schema_gen(
                activities, source_type))
            # print("Validation successful.")
        except Exception as e:
            print(f"Validation failed: {e}")

        # model types
        # check("additional_allowed_model_components", source_type, experiment)

        # # activity
        # check("activity_id", activity_id, experiment)
        # check("parent_activity_id", activity_id, experiment)

        # id
        assert name == experiment.get('experiment_id')



if __name__ == '__main__':
    CV = json.load(open(
        '/Users/daniel.ellis/WIPwork/CVTool/mip_specific/lesf/testdirLESF/cv_cmor/CMIP6Plus_CV.json')).get('CV')
    test(CV)
