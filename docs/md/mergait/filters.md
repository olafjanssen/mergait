Module mergait.filters
======================
Data filters

Functions that help append standard filters to the data, such as detecting running, flat surfaces
and wrongly positioned footpods.

Functions
---------

    
`append_activity_filter(df, df_activity, activity='running', window=[10, -2], new_column='bad_not_running')`
:   Append a filter column to the dataframe based on the 'activity' columns.
    Use this to select only 'walking', 'stationary' or 'running' data.
    
    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame containing the data to append the filter column to
    df_activity : pandas.Dataframe
        The DataFrame containing the phone activity data
    window : list
        A 2-list of a window of time in seconds to pad around the valid values to remove also start-up effects and
        lags in recognizing the correct activity.
    new_column : str
        The name of the filter column to add
    
    Returns
    -------
    pandas.DataFrame
        A new DataFrame with the appended filter column

    
`append_elevation_filter(df, df_activity, window=[-10, 2], new_column='bad_not_flat')`
:   Append a filter column to the dataframe based on the floors in the activity data.
    Use this to select for climbs or flat surfaces.
    
    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame containing the data to append the filter column to
    df_activity : pandas.Dataframe
        The DataFrame containing the phone activity data
    window : list
        A 2-list of a window of time in seconds to pad around the valid values to remove also start-up effects and
        lags in recognizing the correct activity.
    new_column : str
        The name of the filter column to add
    
    Returns
    -------
    pandas.DataFrame
        A new DataFrame with the appended filter column