import json
from jsonschema import validate

# Define your JSON schema
schema = {
    "type": "object",
    "properties": {
        "source_id": {
            "type": "object",
            "patternProperties": {
                ".*": {
                    "type": "object",
                    "properties": {
                        "activity_participation": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            }
                        },
                        "cohort": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            }
                        },
                        "institution_id": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            }
                        },
                        "license_info": {
                            "type": "object",
                            "properties": {
                                "exceptions_contact": {
                                    "type": "string"
                                },
                                "history": {
                                    "type": "string"
                                },
                                "id": {
                                    "type": "string"
                                },
                                "license": {
                                    "type": "string"
                                },
                                "source_specific_info": {
                                    "type": "string"
                                },
                                "url": {
                                    "type": "string"
                                }
                            },
                            "required": ["exceptions_contact", "history", "id", "license", "source_specific_info", "url"]
                        },
                        "source_id": {
                            "type": "string"
                        },
                        "source": {
                            "type": "string"
                        }
                    },
                    "required": ["activity_participation", "cohort", "institution_id", "license_info", "source_id", "source"]
                }
            }
        }
    },
    "required": ["source_id"]
}


 
def check(key, compareset, experiment):
    if set(experiment.get(key)) - compareset:
        raise AssertionError(f"\n\nMissing value: {set(experiment.get(key)) - compareset} \n\n in column '{key}' \n\n for {experiment}")
        



def test(CV):


    # source_type = set(CV.get('source_type'))
    activity_id = set(CV.get('activity_id')).union(set(['no parent']))

    for name, source in CV.get('source_id').items():

        # schema test
        try:
            # Validate the JSON data against the schema
            validate(instance=source, schema=schema)
            print("Validation successful.")
        except Exception as e:
            print(f"Validation failed: {e}")

        # # model types 
        

        # # activity
        check("activity_participation",activity_id,source)
        # check("parent_activity_id",activity_id,experiment)
        
        print(source)
        assert source.get('cohort')[0] in ['Published']

        # id 
        assert name == source.get('source_id')
        

# ISNTITUTION CHECK IN CV CONSTRUCTION        
print('source institution checks happen in the CV creation process.')

if __name__ == '__main__':
    CV = json.load(open('/Users/daniel.ellis/WIPwork/CVTool/mip_specific/lesf/testdirLESF/cv_cmor/CMIP6Plus_CV.json')).get('CV')
    test(CV)