ACCEPTED_VARS = ['branded_variable_name', 'cell_measures', 'cell_methods', 'comment', 
                        'dimensions', 'frequency', 'long_name', 'modeling_realm', 
                        'out_name', 'positive', 'provenance', 'standard_name', 
                        'type', 'units']

tests = {
    'branded_variable_name': lambda x: isinstance(x, str),
    'cell_measures': lambda x: isinstance(x, str),
    'cell_methods': lambda x: isinstance(x, str),
    'comment': lambda x: isinstance(x, str),
    'dimensions': lambda x: isinstance(x, str),
    'frequency': lambda x: isinstance(x, str),
    'long_name': lambda x: isinstance(x, str),
    'modeling_realm': lambda x: isinstance(x, str),
    'ok_max_mean_abs': lambda x: isinstance(x, str) or isinstance(x, float),
    'ok_min_mean_abs': lambda x: isinstance(x, str) or isinstance(x, float),
    'out_name': lambda x: isinstance(x, str),
    'positive': lambda x: isinstance(x, str),
    'provenance': lambda x: isinstance(x, dict),
    'standard_name': lambda x: isinstance(x, str),
    'type': lambda x: isinstance(x, str),
    'units': lambda x: isinstance(x, str),
    'valid_max': lambda x: isinstance(x, str) or isinstance(x, float),
    'valid_min': lambda x: isinstance(x, str) or isinstance(x, float)
}

template = {
    "branded_variable_name": "new_variable_name",
    "cell_measures": "area: areacella",
    "cell_methods": "area: mean time: point",
    "comment": "This is a new variable.",
    "dimensions": "longitude latitude time1",
    "frequency": "3hrPt",
    "long_name": "New Variable",
    "modeling_realm": "atmosphere",
    "ok_max_mean_abs": "",
    "ok_min_mean_abs": "",
    "out_name": "new_var",
    "positive": "up",
    "provenance": {
        "CMIP6": {
            "dreq_uid": "new_uid",
            "mip_table": "E3hrPt",
            "variable_name": "new_variable_name"
        }
    },
    "standard_name": "new_standard_name",
    "type": "real",
    "units": "W m-2",
    "valid_max": "",
    "valid_min": ""
}

