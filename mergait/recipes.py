""" High-level recipes for transforming raw data into statistics
"""
import pandas as pd
import numpy as np

from mergait.symmetry import *
from mergait.filters import *
from mergait.bouts import *
from mergait.music import *
from mergait.stats import *
from mergait.imu import *

import logging

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger("mergait-Recipes")


def filter_to_valid_bouts_recipe(
    df, df_music, df_phone_activity, df_sessions, sections=None
):
    """
    Recipe for filtering valid running bouts per track or section.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing footpod data
    df_music : pandas.DataFrame
        DataFrame containing music playstate data
    df_phone_activity : pandas.DataFrame
        DataFrame containing the phone activity monitor data
    df_sessions : pandas.DataFrame
        DataFrame containing the session bouts
    sections : None or pandas.DataFrame
        If a DataFrame is given, use it to compute the footpod symmetry per music section
        otherwise treat the track as one section

    Returns
    -------
    pandas.DataFrame
        A DataFrame that now includes only valuable/valid data and a bout index per track/section
    """
    df = df.copy()

    # filter pod data on bouts
    df = append_activity_filter(df, df_phone_activity)
    df = append_elevation_filter(df, df_phone_activity)

    # filter pod data with music playstate and merge playstate position
    df = merge_music_playstate(df, df_music)

    # extract valuable run bouts and add a bout index
    valid = ~(
        df["bad_not_running"]
        | df["bad_not_flat"]
        | df["bad_no_music"]
        | df["bad_half_step"]
    )

    # actually filter the steps
    df = df[valid]

    # add session_id
    add_bouts_as_column(
        df, df_sessions, new_column="session_id", valid_column="session_id"
    )

    # extract valid running bouts
    by_bouts = ["session_id", "track_uri"]

    if not sections is None:
        df = append_music_section(df, sections)
        by_bouts.append("section")

    run_bouts = extract_bouts(df, valid, keep_invalid=False, by=by_bouts)
    run_bouts["idx"] = run_bouts.index
    add_bouts_as_column(df, run_bouts, new_column="bout_idx", valid_column="idx")

    return df


def recipe_footpod_symmetry(
    df_footpods, df_music, df_phone_activity, df_sessions, sections=None
):
    """
    Recipe for extracting statistical symmetry information per song for
    valid bouts of running of the real-time footpod data.

    Parameters
    ----------
    df_footpods : pandas.DataFrame
        DataFrame containing footpod data
    df_music : pandas.DataFrame
        DataFrame containing music playstate data
    df_phone_activity : pandas.DataFrame
        DataFrame containing the phone activity monitor data
    df_sessions : pandas.DataFrame
        DataFrame containing the session bouts
    sections : None or pandas.DataFrame
        If a DataFrame is given, use it to compute the footpod symmetry per music section
        otherwise treat the track as one section

    Returns
    -------
    pandas.DataFrame
        The data of all valid gait cycle steps with left and right footpod data
    pandas.DataFrame
        The summarized statistical symmetry data per song (or per section)

    """
    log.debug("[ Computing symmetry information from footpod data")
    df_pods = df_footpods.copy()

    # combine pod data into pod_gait and annotate bad steps
    df_pod_steps = merge_left_right_data(df_pods)

    df_pod_steps = filter_to_valid_bouts_recipe(
        df_pod_steps, df_music, df_phone_activity, df_sessions, sections=sections
    )

    df_pod_steps = append_symmetry_index(df_pod_steps, method="sa")

    by_bouts = ["session_id", "track_uri"]
    if not sections is None:
        by_bouts.append("section")

    log.debug("Computing aggregate statistics per song/section")

    # now convert to statistical summary per song/section
    summary = df_pod_steps.groupby(by=by_bouts, sort=False).agg(
        ["mean", "std", "median", iqr, rmse, mae]
    )
    summary.columns = summary.columns.map("_".join)
    df_pod_symmetry = summary.reset_index()

    log.debug(
        "] Done, computed symmetry for {} cycles in {} songs/sections".format(
            len(df_pod_steps), len(df_pod_symmetry)
        )
    )

    return [df_pod_steps, df_pod_symmetry]


def recipe_imu_symmetry(
    df_imu, df_music, df_phone_activity, df_sessions, sections=None
):
    """
    Recipe for extracting statistical symmetry information per song for
    valid bouts of running of the real-time imu data.

    Parameters
    ----------
    df_footpods : pandas.DataFrame
        DataFrame containing footpod data
    df_music : pandas.DataFrame
        DataFrame containing music playstate data
    df_phone_activity : pandas.DataFrame
        DataFrame containing the phone activity monitor data
    df_sessions : pandas.DataFrame
        DataFrame containing the session bouts
    sections : None or pandas.DataFrame
        If a DataFrame is given, use it to compute the footpod symmetry per music section
        otherwise treat the track as one section

    Returns
    -------
    pandas.DataFrame
        The data of all valid gait cycle steps with left and right footpod data
    pandas.DataFrame
        The summarized statistical symmetry data per song (or per section)

    """
    log.debug("[ Computing symmetry information from imu vertical acceleration")

    df_acc = df_imu.copy()
    t_acc, a_vert = pd.to_numeric(df_acc["t"]), df_acc["a_vert"]

    df_imu_steps, ic_times_ns, fc_times_ns = gait_features_from_vertical_acceleration(
        t_acc, a_vert
    )

    # assign foot names (we don't know whether it is left or right) so we can compute symmetry
    df_imu_steps["foot"] = "A"
    df_imu_steps["foot"][1::2] = "B"

    df_imu_steps = merge_left_right_data(df_imu_steps, feet=["A", "B"], side="both")

    df_imu_steps = filter_to_valid_bouts_recipe(
        df_imu_steps, df_music, df_phone_activity, df_sessions, sections=sections
    )

    df_imu_steps = append_symmetry_index(df_imu_steps, method="sa")

    by_bouts = ["session_id", "track_uri"]
    if not sections is None:
        by_bouts.append("section")

    # now convert to statistical summary per song/section
    log.debug("Computing aggregate statistics per song/section")

    summary = df_imu_steps.groupby(by=by_bouts, sort=False).agg(
        ["mean", "std", "median", iqr, rmse, mae]
    )
    summary.columns = summary.columns.map("_".join)
    df_imu_symmetry = summary.reset_index()

    # now also add gsi information
    if sections is None:
        df_gsi_bouts = compute_gsi_from_imu_recipe(
            df_imu_steps, df_imu, by=["track_uri", "session_id"]
        )
    else:
        df_gsi_bouts = compute_gsi_from_imu_recipe(df_imu_steps, df_imu)

    df_gsi_summary = (
        df_gsi_bouts.drop("bout_idx", axis=1)
        .groupby(by=by_bouts, sort=False)
        .agg(["mean", "median"])
    )
    df_gsi_summary.columns = df_gsi_summary.columns.map("_".join)
    df_gsi_symmetry = df_gsi_summary.reset_index()

    df_imu_symmetry = df_imu_symmetry.merge(df_gsi_symmetry, on=by_bouts)

    log.debug(
        "] Done, computed symmetry for {} cycles in {} songs/sections".format(
            len(df_imu_steps), len(df_imu_symmetry)
        )
    )

    return [df_imu_steps, df_imu_symmetry]


def compute_gsi_from_imu_recipe(df, df_imu, by=["track_uri", "session_id", "section"]):
    """
    Recipe for computing the gait symmetric index (GSI) from bouts of imu data.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame bout information
    df_imu : pandas.DataFrame
        DataFrame containing the phone imu data
    by : pandas.DataFrame
        Columns to group the data by

    Returns
    -------
    pandas.DataFrame
        A Dataframe containing the gsi and related stride duration and cadence for
        every bout in the given DataFrame
    """
    log.debug("[ Following recipe to compute Gait Symmetry Index per running bout")

    agg_funs = {"t": ["first", "last"]}
    for b in by:
        agg_funs[b] = "first"

    # group by bout, to compute the gsi only for a continuous stretch of data
    df_gsi_bouts = df.groupby("bout_idx").agg(agg_funs).reset_index()

    def apply_gsi(row):
        df_acc = df_imu[(df_imu.t > row.t[0]) & (df_imu.t < row.t[1])]
        gsi, stride_duration = gait_symmety_index_from_acceleration(
            df_acc.ax, df_acc.ay, df_acc.az
        )
        return gsi, stride_duration * 1000, 2 * 60 / stride_duration

    # perform the gsi computation per bout
    df_gsi_bouts[["gsi", "stride_duration", "cadence"]] = df_gsi_bouts.apply(
        apply_gsi, axis=1, result_type="expand"
    )

    # clean up return DataFrame
    df_gsi_bouts.columns = [c[0] for c in df_gsi_bouts.columns]
    df_gsi_bouts.drop(["t"], axis=1, inplace=True)

    log.debug("] Computed the gsi for {} bouts".format(len(df_gsi_bouts)))
    return df_gsi_bouts
