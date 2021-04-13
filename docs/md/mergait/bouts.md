Module mergait.bouts
====================
Bout utility methods

Methods for extracting bouts from DataFrames and annotating other DataFrames
with this bout information.

A bout is a time range within a larger set of data that shares a particular feature.

Functions
---------

    
`add_bouts_as_column(df, bouts, new_column='bout', range_column='t', valid_column='valid', value='column', reset_value=Series([], dtype: float64))`
:   Applies the time ranges in a bouts DataFrame created with `extract_bouts` to the rows in another DataFrame, by
    adding bout data to a new column.
    
    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame containing the data that has to be annotated by bout information
    bouts : pandas.Dataframe
        The DataFrame containing the bouts
    new_column : str
        The optional column name to add with bout information
    range_column : str
        Optional string indicating the column in original for the timestamp. This results in a prefix
        in the bouts DataFrame, timestamp column 't' leads to bout columns 't_start' and 't_end'.
    valid_column : str
        Optional string indicating the name in the output DataFrame indicating the validness of the bout
    value : object
        Optional value to insert for a valid bout. If 'index' it takes the bout index as bout identifier,
        'column' fills in the valid column else sets the constant value given.
    reset_value : object
        Optional default value set to the new bouts column if it does not yet exist
    
    Returns
    -------
    pandas.DataFrame
        A reference to the updated df DataFrame. The original DataFrame is updated in place.

    
`extract_bouts(df, valid, range_column='t', valid_column='valid', keep_invalid=True, by=[])`
:   Extract from a Pandas DataFrame a list of bouts, where each bout is indicated by a minimum and maximum
    timestamp range and determined by valid ranges.
    
    Parameters
    ----------
    df : pandas.Dataframe
        The data to extract the bouts from
    valid : pandas.Series
        A series of bool values indicating what rows are considered valid and invalid
    range_column : str
        Optional string indicating the column in df for the timestamp
    valid_column : str
        Optional string indicating the name in the output DataFrame indicating the validness of the bout
    keep_invalid : bool
        Optional value indicating whether to keep invalid bouts in the returned DataFrame
    by : list
        Optional list of columns to group the data by, before extracting the bouts, meaning that bout
        boundaries are both determined by the valid column and the group boundaries.
    
    Returns
    -------
    pandas.DataFrame
        Index:
            RangeIndex
        Columns:
            Name: count, dtype: int64
                Number of rows in df belonging to the bout
            Name: t_start, dtype: datetime64[ns]
                Starting timestamp of the bout (t_ prefix depends on range_column)
            Name: t_end, dtype: datetime64[ns]
                End timestamp of the bout (t_ prefix depends on range_column)
            Name: valid, dtype: bool
                Whether the bout is valid according to given criterium

    
`interpolate_bouts_as_column(df, df_values, bouts, new_column='bout', range_column='t', valid_column='valid', value_column='position', reset_value=Series([], dtype: float64))`
:   Applies the time ranges in a bouts DataFrame created with `extract_bouts` to the rows in another DataFrame, by
    adding bout data to a new column.
    
    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame containing the data that has to be annotated by bout information
    bouts : pandas.Dataframe
        The DataFrame containing the bouts
    df_values : pandas.DataFrame
        The DataFrame containing the values to interpolate into df
    value_column : str
        The column in df_values with the values to interpolate into df
    new_column : str
        The optional column name to add with bout information
    range_column : str
        Optional string indicating the column in original for the timestamp. This results in a prefix
        in the bouts DataFrame, timestamp column 't' leads to bout columns 't_start' and 't_end'.
    valid_column : str
        Optional string indicating the name in the output DataFrame indicating the validness of the bout
    reset_value : object
        Optional default value set to the new bouts column if it does not yet exist
    
    Returns
    -------
    pandas.DataFrame
        A reference to the updated df DataFrame. The original DataFrame is updated in place.

    
`select_range(df, window, range_column='t', include_end=True)`
:   Select a range of data for multiple Pandas DataFrames at once.
    It was designed for using it with the output of the bout methods.
    
    Parameters
    ----------
    df : pandas.DataFrame/list
        The (list of) DataFrame to use
    window : list
        A 2-list containing the minimum and maximum value of the range to select
    range_column : str
        Optional column in the DataFrame to use for the range (usually timestamp)
    include_end : bool
        Optional whether to include the max value in the range
    
    Returns
    -------
    list(pandas.DataFrame)
        A list of DataFrames selections

    
`with_padded_bout_window(bouts, window=[0, 0], range_column='t')`
:   Pad the values in a Pandas DataFrame created with `extract_bouts` with a time window.
    
    Parameters
    ----------
    bouts : pandas.Dataframe
        The DataFrame containing the bouts
    window : list
        The number of seconds to add to the starting and end time of the bout.
    range_column : str
        Optional string indicating the column in original for the timestamp. This results in a prefix
        in the bouts DataFrame, timestamp column 't' leads to bout columns 't_min' and 't_max'.
    
    Returns
    -------
    pandas.DataFrame
        A copy of the bouts DataFrame with padded min and max timestamp values