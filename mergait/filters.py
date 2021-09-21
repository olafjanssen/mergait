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
    df = df.copy()

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


def append_session_filters(
    df_sessions,
    df_footpods,
    impact_column="impact",
    pronation_column="pronation",
    flight_ratio_column="flight_ratio",
):
    """
    Append filter columns to the sessions DataFrame. These filters indicate an entire failed session, from the perspective of the footpod data.

    Parameters
    ----------
    df_sessions : pandas.DataFrame
        The DataFrame containing the sessions data to append the filter column to
    df_footpods : pandas.Dataframe
        The DataFrame containing the footpod data
    impact_column : str
        Name of the column indicating the foot impact
    pronation_column : str
        Name of the column indicating the foot pronation
    flight_ratio_column : str
        Name of the column indicating the foot flight ratio

    Returns
    -------
    pandas.DataFrame
        A new DataFrame with the appended filter columns
    """
    df = df_footpods.copy()

    # add session_id to footpod data
    add_bouts_as_column(
        df, df_sessions, new_column="session_id", valid_column="session_id"
    )

    session_means = df.groupby("session_id").mean().reset_index()

    filter_frame = pd.DataFrame(
        data={
            "session_id": session_means.session_id,
            "bad_pods_upside_down": session_means[impact_column] < 5,
            "bad_pods_switched_sides": session_means[pronation_column] > 0,
            "bad_fake_run": session_means[flight_ratio_column] < 1,
        }
    )

    df_sessions = df_sessions.merge(filter_frame, on=["session_id"], how="right")

    return df_sessions


def apply_session_filters(df, df_footpods):
    """
    Filter invalid sessions based on footpod data.

    Parameters
    ----------
    df_sessions : pandas.DataFrame
        The DataFrame containing the sessions data to append the filter column to
    df_footpods : pandas.Dataframe
        The DataFrame containing the footpod data

    Returns
    -------
    pandas.DataFrame
        A new DataFrame with only valid sessions
    """
    df = df.copy()

    df = append_session_filters(df, df_footpods)

    # extract valuable run bouts and add a bout index
    valid = ~(
        df["bad_pods_upside_down"] | df["bad_pods_switched_sides"] | df["bad_fake_run"]
    )

    # actually filter the steps
    df = df[valid]

    return df
