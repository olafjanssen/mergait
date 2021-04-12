""" 
General utility functions for handling the data
"""

import pandas as pd


def load_datadumps(paths, timestamp_columns=["t"], file_type="csv", base_path=""):
    """
    Load one or more datadump files into Pandas DataFrames.
    It additionally parses date columns and sorts by timestamp.

    Parameters
    ----------
    paths : str/list
        If str then load a single file, otherwise process all in the given list
    timestamp_columns : list
        Optional list of columns to parse as timestamp
    file_type : str
        Optional type of the datadump file, defaults to csv
    base_path : str
        Optional path to append to all filename paths given in the first argument

    Returns
    -------
    list(pandas.DataFrame)
        A list of DataFrames corresponding to the given paths
    """
    dfs = []

    for path in paths if isinstance(paths, list) else [paths]:
        df = pd.read_csv(base_path + path, parse_dates=timestamp_columns)
        if len(timestamp_columns) > 0:
            df.sort_values(by=timestamp_columns[0], inplace=True)
        df.reset_index(drop=True, inplace=True)
        dfs.append(df)

    return dfs if isinstance(paths, list) else dfs[0]