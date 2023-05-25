import json

def create(MIPname,sourceId,experimentId,activityId,region, baseLocation,writeLocation):

    assert baseLocation[-1] == '/'
    assert writeLocation[-1] == '/'

    CVs = json.load(open(f'{baseLocation}{MIPname}_CV.json'))['CV']
                     
    assert sourceId in CVs['source_id']
    assert activityId in CVs['activity_id']


    template = {
        "#note":           "explanation of what source_type is goes here",
        "source_type":            "AOGCM AER",
    
        "#note":                  "CMIP6 valid experiment_ids are found in CMIP6_CV.json",
        "activity_id":            f"{activityId}",
        "region":                 f"{region}",
        "realization_index":      "3",
        "initialization_index":   "1",
        "physics_index":          "1",
        "forcing_index":          "1",
    
        "#note":                  "Text stored in attribute variant_info (recommended, not 
required description of run variant)",
        "run_variant":            "3rd realization",

        "parent_activity_id":     "CMIP",
        "parent_source_id":       f"{sourceId}",
        "parent_variant_label":   "r3i1p1f1",
    
        "parent_time_units":      "days since 1850-01-01",
        "branch_method":          "standard",
        "branch_time_in_child":   59400.0,
        "branch_time_in_parent":  59400.0,
    
        "#note":                  "institution_id must be registered at 
https://github.com/WCRP-CMIP/CMIP6_CVs/issues/new ",
        "institution_id":         "MOHC",
    
        "#note":                  "source_id (model name) must be registered at 
https://github.com/WCRP-CMIP/CMIP6_CVs/issues/new ",
        "source_id":              f"{sourceId}",
    
        "calendar":               "360_day",
    
        "grid":                   "native atmosphere regular grid (3x4 latxlon)",
        "grid_label":             "gn",
        "nominal_resolution":     "10000 km",
    
        "license": "CMIP6Plus model data produced by MOHC is licensed under a Creative 
Commons  License (https://creativecommons.org/). Consult 
https://pcmdi.llnl.gov/CMIP6Plus/TermsOfUse for terms of use governing CMIP6Plus output, 
including citation requirements and proper acknowledgment. Further information about this 
data, including some limitations, can be found via the further_info_url (recorded as a 
global attribute in this file). The data producers and data providers make no warranty, 
either express or implied, including, but not limited to, warranties of merchantability and 
fitness for a particular purpose. All liabilities arising from the supply of the information 
(including any liability arising in negligence) are excluded to the fullest extent permitted 
by law.",
    
        "#output":                "Root directory for output (can be either a relative or 
full path)",
        "outpath":                ".",
    
        "#note":                  " **** The following descriptors are optional and may be 
set to an empty string ",  
    
        "contact ":               "Python Coder (coder@a.b.c.com)",
        "history":                "Output from archivcl_A1.nce/giccm_03_std_2xCO2_2256.",
        "comment":                "",
        "references":             "Model described by Koder and Tolkien (J. Geophys. Res., 
2001, 576-591).  Also see http://www.GICC.su/giccm/doc/index.html.  The ssp245 simulation is 
described in Dorkey et al. '(Clim. Dyn., 2003, 323-357.)'",
    
        "#note":                  " **** The following will be obtained from the CV and do 
not need to be defined here", 
    
        "institution":            "",
        "source":                 "PCMDI-test 1.0 (1989)",
    
        "#note":                  " **** The following are set correctly for CMIP6 and 
should not normally need editing",  
    
        "_controlled_vocabulary_file":f"{baseLocation}{MIPname}_CV.json",
        "_AXIS_ENTRY_FILE":         f"{baseLocation}{MIPname}_coordinate.json",
        "_FORMULA_VAR_FILE":        f"{baseLocation}{MIPname}_formula_terms.json",
        "_cmip6_option":           "CMIP6",
    
        "mip_era":                "CMIP6Plus",
        "parent_mip_era":         "CMIP6Plus",
    
        "tracking_prefix":        "hdl:21.14100",
        "_history_template":       "%s ;rewrote data to be consistent with <activity_id> for 
variable <variable_id> found in table <table_id>.",
    
        "#output_path_template":   "Template for output path directory using tables keys or 
global attributes, these should follow the relevant data reference syntax",
        "output_path_template":    
"<mip_era><activity_id><institution_id><source_id><_member_id><table><variable_id><grid_label><version>",
        "output_file_template":    "<variable_id><table><source_id><_member_id><grid_label>"
    }



    filename = f"{writeLocation}{MIPname}_input.json"

    # Writing JSON data with indentation and colons aligned
    with open(filename, "w") as outfile:
        json.dump(template, outfile, indent="\t", separators=(",",": " ))

    return filename



