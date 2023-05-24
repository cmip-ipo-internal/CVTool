
import re, os
import shutil
import pprint
import configparser
import pandas as pd

from ..core.stdout import log
print = log(__file__.split('cvtool')[1])


class ESGFIni:
    """
    A class to parse and access data from an ESGF INI configuration file

    Attributes:
        project (str): The project name of the INI file
        categories (pandas.DataFrame): A DataFrame containing information about the categories of each key
        headers (List[str]): A list of the headers for the INI file
    """

    def __init__(self, ini_file: str) -> None:
        """
        Initializes the class by reading the INI file and parsing the data

        Args:
            ini_file (str): The file path to the INI file to be parsed
        """
        assert os.path.exists(ini_file)
        self._complete = read_esgf_ini(ini_file)
        self.project = list(self._complete)[0]
        self._esgf_data = self._complete.get(self.project)
        self.headers = list(self._esgf_data)
        self.categories = categories(self._esgf_data.get('categories'))
        self._flatten_data = {}
        self._flatten_keys(self._esgf_data, '')

    def __getattr__(self, key: str):
        """
        Overrides the default behavior of getting an attribute from the class to get data from the INI file.

        Args:
            key (str): The key to get from the INI file.

        Returns:
            The value of the key in the INI file.

        Raises:
            AttributeError: if the key is not found in the INI file.
        """
        if key in self._flatten_data:
            return self._flatten_data[key]
        raise AttributeError(f"'ESGFData' object has no attribute '{key}'")

    def _flatten_keys(self, data: dict, prefix: str) -> None:
        """
        Recursively flattens the keys of the INI file to make them accessible as attributes of the class.

        Args:
            data (dict): The data of the INI file.
            prefix (str): The prefix to add to each key.
        """
        for key, value in data.items():
            if isinstance(value, dict):
                new_prefix = f"{prefix}{key}."
                self._flatten_keys(value, new_prefix)
            elif '|' in value:
                value = cfg2obj(value, False)
            elif ', ' in value and '%' not in value:
                value = value.split(', ')
            self._flatten_data[f"{prefix}{key}"] = value

    def print(self,key):
        '''
        Set up pretty print formatting scaling to the width of the terminal. 

        Example usage: 
            ```class.print('experiment_title_map')```

        '''
        terminal_width = shutil.get_terminal_size().columns
        return pprint.pprint(cmip6.__getattr__(key), width = terminal_width)


'''
Single use functions: 
    We do not want to package these up with the class and propagate them forwards. 
'''

def read_esgf_ini(file_path: str) -> dict:
    """
    Reads the INI file and turns it into a dictionary.

    Args:
        file_path (str): The file path to the INI file to be parsed.

    Returns:
        A dictionary containing the data from the INI file.
    """
    config = configparser.ConfigParser(interpolation=None)
    config.read(file_path)
    esgf_data = {}
    for section in config.sections():
        section_data = {}
        for key, value in config.items(section):
            section_data[key] = value
        esgf_data[section] = section_data
    return esgf_data


def categories(categories_str: str) -> pd.DataFrame:
    """
    Parses the categories string from the INI file and turns it into a DataFrame.

    Args:
        categories_str (str): The categories string from the INI file.

    Returns:
        A DataFrame containing information about the categories of each key.
    """
    pattern = r"\s+(\w+)\s+\|\s+(\w+)\s+\|\s+(\w+)\s+\|\s+(\w+)\s+\|\s+(\d+)"
    matches = re.findall(pattern, categories_str)
    df = pd.DataFrame(
        matches,
        columns=["Column", "Type", "Required", "Used", "Priority"]
    )
    df = df.astype({
        "Column": str,
        "Type": str,
        "Required": bool,
        "Used": bool,
        "Priority": int
    })
    return df.set_index('Column', inplace=False)


def cfg2obj(config_str: str, dataseries: bool = False):
    """
    Parses a configuration string and turns it into a dictionary or a DataFrame.

    Args:
        config_str (str): The configuration string to be parsed.
        dataseries (bool, optional): Whether or not to return a DataFrame. Defaults to False.

    Returns:
        The parsed configuration string as a dictionary or a DataFrame.
    """
    pattern = r"([^\s|]+)\s*\|\s*([^|]+)"
    matches = re.findall(pattern, config_str)
    data = {key.strip(): value.strip() for key, value in matches}
    if dataseries:
        df = pd.DataFrame.from_dict(data, orient="index", columns=["value"])
        df.index.name = "key"
        return df
    return data




# if __name__ == '__main__':
#     base = '/Users/daniel.ellis/WIPwork/esgf-config/publisher-configs/ini/'
#     path = f'{base}esg.cmip6.ini'
#     cmip6 = ESGFIni(path)