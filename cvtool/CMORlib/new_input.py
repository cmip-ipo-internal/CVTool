import json
from .. import core

key2str = lambda x : ' '.join(list(x.keys()))

def create(cvfile, institution, baseLocation, writeLocation, region='moon', history= None, comment = None,references = None ):
        

    assert writeLocation[-1] == '/'

    CVs = json.load(open(cvfile))['CV']
                     
    sourceid = list(CVs.keys())[0]
    print('warn - sourceid [0] only')


    template = {
        "#note":           "explanation of what source_type is goes here",
        "source_type":            key2str(CVs['source_type']),
    
        "#note":                  "CMIP6 valid experiment_ids are found in CMIP6_CV.json",
        "activity_id":            CVs['activity_id'],
        "region":                 region,
        "realization_index":      "3",
        "initialization_index":   "1",
        "physics_index":          "1",
        "forcing_index":          "1",
    
        "#note":                  "Text stored in attribute variant_info (recommended, not required description of run variant)",
        "run_variant":            "3rd realization",

        "parent_activity_id":     "CMIP",
        "parent_source_id":       sourceid,
        "parent_variant_label":   "r3i1p1f1",
    
        "parent_time_units":      "days since 1850-01-01",
        "branch_method":          "standard",
        "branch_time_in_child":   59400.0,
        "branch_time_in_parent":  59400.0,
    
        "#note":                  "institution_id must be registered at https://github.com/WCRP-CMIP/CMIP6_CVs/issues/new ",
        "institution_id":         key2str(CVs['institution_ids']),
    
        "#note":                  "source_id (model name) must be registered at https://github.com/WCRP-CMIP/CMIP6_CVs/issues/new ",
        "source_id":              source_id,
    
        "calendar":               "360_day",
    
        "grid":                   "native atmosphere regular grid (3x4 latxlon)",
        "grid_label":             "gn",
        "nominal_resolution":     "10000 km",
    
        "license": CVs['lisence'],
    
        "#output":                "Root directory for output (can be either a relative or full path)",
        "outpath":                ".",
    
        "#note":                  " **** The following descriptors are optional and may be set to an empty string ",  
    
        "contact ":               core.stdout.get_user()['user'],
        "history":                history or "",
        "comment":                comment or "",
        "references":             references or "",
    
        "#note":                  " **** The following will be obtained from the CV and do not need to be defined here", 
    
        "institution":            institution,
        "source":                 "PCMDI-test 1.0 (1989)",
    
        "#note":                  " **** The following are set correctly for CMIP6 and should not normally need editing",  
    
        "_controlled_vocabulary_file":cvfile,
        "_AXIS_ENTRY_FILE":         f"{baseLocation}{MIPname}_coordinate.json",
        "_FORMULA_VAR_FILE":        f"{baseLocation}{MIPname}_formula_terms.json",
        "_cmip6_option":           "CMIP6",
    
        "mip_era":                CVs['mip_era'],
        "parent_mip_era":         CVs['mip_era'],
    
        "tracking_prefix":        "hdl:21.14100",
        "_history_template":       "%s ;rewrote data to be consistent with <activity_id> for variable <variable_id> found in table <table_id>.",
    
        "#output_path_template":   "Template for output path directory using tables keys or global attributes, these should follow the relevant data reference syntax",
        "output_path_template":    
"<mip_era><activity_id><institution_id><source_id><_member_id><table><variable_id><grid_label><version>",
        "output_file_template":    "<variable_id><table><source_id><_member_id><grid_label>"
    }



    filename = f"{writeLocation}input.json"

    # Writing JSON data with indentation and colons aligned
    with open(filename, "w") as outfile:
        json.dump(template, outfile, indent="\t", separators=(",",": " ))

    return filename



