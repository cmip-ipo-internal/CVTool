import json
from typing import List, Optional, Union
from copy import deepcopy



fields = {
  'Required Variables': {
    'mip_era': 'enum',
    'activity_drs': 'enum',
    'institution_id': 'enum',
    'source_id': 'enum',
    'experiment_id': 'enum',
    'member_id': 'string',
    'table_id': 'enum',
    'variable_id': 'string',
    'grid_label': 'enum',
    'model_cohort': 'string'
  },
  'Optional Variables': {
    'frequency': 'string',
    'realm': 'string',
    'product': 'string',
    'nominal_resolution': 'string',
    'source_type': 'string',
    'grid': 'string',
    'creation_date': 'string',
    'variant_label': 'string',
    'sub_experiment_id': 'enum',
    'further_info_url': 'string',
    'activity_id': 'string',
    'data_specs_version': 'string',
    'experiment_title': 'string',
    'project': 'string',
    'description': 'text'
  }
}


experiment_template = {
    "activity_id": [],
    "additional_allowed_model_components": [],
    "experiment": "",
    "experiment_id": "",
    "parent_activity_id": [],
    "parent_experiment_id": [],
    "required_model_components": [],
    "sub_experiment_id": "none",
}


class CVClass:
    """
    Class for manipulating CV JSON content.
    """
    def __init__(self, json_path: str) -> None:
        """
        Constructor method that reads CV JSON from file path.

        Args:
            json_path: The path to the JSON file.
        """
        with open(json_path) as f:
            self.json_content = json.load(f)['CV']

    def write_json(self, json_path: str) -> None:
        """
        Write the CV JSON object to file at specified path.

        Args:
            json_path: The path to write the JSON file to.
        """
        with open(json_path, "w") as f:
            json.dump(dict(Cv=self.json_content), f)

    def add_activity(self, activity_id: str, experiment_id: Optional[str]=None):
        """
        Method to add a new activity (if it doesn't already exist) to the CV JSON content.

        Args:
            activity_id: The ID of the activity to add.
            experiment_id: The ID of the experiment to add.

        Returns:
            None
        """
        if activity_id not in self.json_content:
            self.json_content[activity_id] = []
        
        if experiment_id and experiment_id not in self.json_content:
            self.json_content[activity_id].append(experiment_id)

    def add_experiment(self, **kwargs) -> None:
        """
        Adding, or modifying an experiment. 

        Args:
            activity_id: List of activity IDs.
            additional_allowed_model_components: List of additional allowed model components.
            experiment: Experiment name.
            experiment_id: Experiment ID.
            parent_activity_id: List of parent activity IDs.
            parent_experiment_id: List of parent experiment IDs.
            required_model_components: List of required model components.
            sub_experiment_id: Sub-experiment ID.

        Raises:
            TypeError: If any input has an invalid type.

        Examples:
            >>> template = populate_template(
            ...     activity_id=["act1", "act2"],
            ...     experiment="exp1",
            ...     experiment_id="exp_id1",
            ...     required_model_components=["comp1", "comp2"],
            ... )

            {
                "activity_id": ["act1", "act2"],
                "additional_allowed_model_components": [],
                "experiment": "exp1",
                "experiment_id": "exp_id1",
                "parent_activity_id": [],
                "parent_experiment_id": [],
                "required_model_components": ["comp1", "comp2"],
                "sub_experiment_id": "none",
            }
        """
        # Check that the experiment id exists
        assert 'experiment_id' in kwargs,  'You cannot add an experiment without an experiment id'

        if kwargs['experiment_id'] not in self.json_content:
            # This is a new entry, so we check we have the minimum required information to add an entry 
            required = {'activity_id', 'experiment', 'required_model_components'}
            missing = required - set(kwargs.keys())
            if not len(missing):
                KeyError(f'You need to supply a dictionary with the following items: {missing}')
            
            # Create the base template
            self.json_content[kwargs['experiment_id']] = deepcopy(experiment_template)
            
        experiment_entry = self.json_content[kwargs['experiment_id']]
        
        # Add activity if it does not already exist
        self.add_activity(kwargs['activity_id'], kwargs['experiment_id'])

        # Required, non-list variables
        str_vars = ('experiment', 'experiment_id')
        for name in str_vars:
            experiment_entry[name] = kwargs[name]

        for entry in kwargs:
            if entry in str_vars:
                continue

            if not isinstance(kwargs[entry], list):
                kwargs[entry] = [kwargs[entry]]

            experiment_entry[entry].extend(kwargs[entry])
        
            # Check that sources are correct
            if 'components' in entry:
               assert all(cmp in self.json_content.get('source_type') for cmp in kwargs[entry]), f"Invalid components from source_type. Please check these against: {kwargs['entry']}"
   


if __name__ == '__main__':
        
    cv = CVTool("/Users/daniel.ellis/WIPwork/mip-cmor-tables/mip_cmor_tables/out/CMIP6Plus_CV.json")




def test_add_activity():
    tool = CVTool('path/to/json')
    tool.json_content = {}
    tool.add_activity('a1')
    assert 'a1' in tool.json_content.keys() 

def test_add_experiment():
    tool = CVTool('path/to/json')
    tool.json_content = {}
    activity_id = ['act1', 'act2']
    entry = {'activity_id': activity_id, 'experiment': 'exp1', 'experiment_id': 'exp_id1', 'required_model_components': ['comp1', 'comp2']}
    tool.add_experiment(**entry)
    assert 'exp_id1' in tool.json_content.keys()
    for act_id in activity_id:
        assert 'exp_id1' in tool.json_content[act_id]

def test_add_experiment_missing_required():
    tool = CVTool('path/to/json')
    tool.json_content = {}
    activity_id = ['act1', 'act2']
    entry = {'activity_id': activity_id, 'experiment': 'exp1', 'experiment_id': 'exp_id1'}
    try:
        tool.add_experiment(**entry)
    except KeyError as e:
        assert 'required_model_components' in str(e)

def test_add_experiment_wrong_source_type():
    tool = CVTool('path/to/json')
    tool.json_content = {'source_type': ['comp1']}
    activity_id = ['act1', 'act2']
    entry = {'activity_id': activity_id, 'experiment': 'exp1', 'experiment_id': 'exp_id1', 'components': ['comp1', 'comp2']}
    try:
        tool.add_experiment(**entry)
    except AssertionError as e:
        assert 'comp2' in str(e)