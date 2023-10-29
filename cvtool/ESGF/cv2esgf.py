import json
import os
import re
import glob
from collections import Counter

# pip install -e git://github.com/ESGF/esgf-prepare.git@master#egg=esgprep

from ESGConfigParser import SectionParser, build_line, lengths
from constants import FILENAME_FORMAT, DATASET_ID # Import constants

"""
Convert CMIP6 CV json files to an ESGConfigParser ini file
"""

def read_cv(cvdir=None, cvfile=None):
    """
    Read CMIP6 CV json files
    
    Params:
        cvdir: Base directory containing CV json files
        cvfile: Single CV json file
        
    Returns: 
        project: CMIP6 project ID
        cv: Dict containing parsed CV data
    """
    
    cv = {}
    
    if cvdir and cvfile:
        print("Both CVDIR and CVFILE defined, using CVDIR")

    if cvdir:
        # Read all json files in cvdir
        project = Counter([f.split("/")[-1].split("_")[0] for f in glob.glob(f"{cvdir}/*.json")]).most_common()[0][0]
        for f in glob.glob(f"{cvdir}/*.json"):
            section = f.split("/")[-1].replace(".json", "")
            cv[section] = json.load(open(f, "r"))

    elif cvfile:
        # Read single CV json file
        project = re.search("/(\w+)_CV.json", cvfile)[1]  
        cv = json.load(open(cvfile, "r"))

    return project, cv

def get_options(cv, section):
    """Extract comma separated list of options from CV section"""
    return ", ".join(sorted(cv[section].keys()))

def get_map(cv, section, key):
    """
    Extract key:value map from CV section
    
    Format as:
        map(key : value)
            value1
            value2
            ...
    """
    header = f"map({section} : {key})" 
    lines = [f"{k}: {v.get(key)}" for k, v in sorted(cv[section].items())]
    return build_line((header,) + tuple(lines), sep="\n", indent=True)
    
if __name__ == "__main__":

    # Constants
    CVFile = "/Users/daniel.ellis/WIPwork/CVTool/mip_specific/lesf/LESF_CVs/merged_data/CVs/CMIP6Plus_CV.json"
    OUTDIR = "./"
    PROJECT = "CMIP6" 

    # Read CV 
    project, cv = read_cv(cvfile=CVFile)

    # Create config
    config = SectionParser(section=f"project:{PROJECT}")

    # Populate options
    config.set("filename_format", FILENAME_FORMAT)
    config.set("dataset_id", DATASET_ID)
    
    config.set("mip_era_options", get_options(cv, "mip_era"))
    config.set("activity_drs_options", get_options(cv, "activity_id"))

    config.set("experiment_title_map", get_map(cv, "experiment_id", "experiment"))
     
    # Write ini file
    with open(f"{OUTDIR}/{PROJECT}.ini", "w") as f:
        config.write(f)