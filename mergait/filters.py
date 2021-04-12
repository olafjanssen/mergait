""" Data filters

Functions that help append standard filters to the data, such as detecting running, flat surfaces
and wrongly positioned footpods.
"""

import pandas as pd
from mergait.bouts import *


def append_activity_filter(
    df, df_activity, activity="running", window=[10, -2], new_column="bad_not_running"
):
    """
    Append a filter column to the dataframe based on the 'activity' columns.
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
    """
    df = df.copy()

    valid = df_activity["activity"] == activity
    bouts = extract_bouts(df_activity, valid, keep_invalid=False)
    add_bouts_as_column(
        df,
        with_padded_bout_window(bouts, window=window),
        new_column=new_column,
        value=False,
        reset_value=True,
    )

    return df


def append_elevation_filter(
    df, df_activity, window=[-10, 2], new_column="bad_not_flat"
):
    """
    Append a filter column to the dataframe based on the floors in the activity data.
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
    """
    df = pd.DataFrame(df)

    floors = df_activity["floors_ascended"] + df_activity["floors_descended"]
    valid = floors.diff() != 0
    bouts = extract_bouts(df_activity, valid, keep_invalid=False)
    add_bouts_as_column(
        df,
        with_padded_bout_window(bouts, window=window),
        new_column=new_column,
        value=True,
        reset_value=False,
    )

    return df
