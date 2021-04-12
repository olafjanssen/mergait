""" Methods that extract features from imu data.
"""

import numpy as np
import pandas as pd
from mergait.stats import *

import logging

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger("MerGait")


def gait_features_from_vertical_acceleration(
    timestamps, a_vert, contact_time_range=[50, 200], step_time_range=[200, 1000]
):
    """
    Extract gait features from the vertical acceleration of a IMU alone.
    It detects initial contact of the foot on the ground and the final contact point and uses
    this to compute step and stride variability.

    Note: This is a rather simplified algorithm based on peak finding. The advantage is that it gives
    rather robust results independent of the sensor position on the body. The disadvantage is that the
    detected contact times may not be an exact value that you could get with foodpod sensors, however the values
    can be used to obtain more relative symmetry information.

    Parameters
    ----------
    timestamps : list
        List of timestamps [ns]
    a_vert : list
        List with the same length as the timestamps with the vertical acceleration component
    df_phone_activity : pandas.DataFrame
        DataFrame containing the phone activity monitor data
    contact_time_range : list
        A 2-list specifying the minimum and maximum expected contact time of a foot [ms]
    step_time_range : list
        A 2-list specifying the minimum and maximum expected duration of a step [ms]

    Returns
    -------
    pandas.DataFrame
        Index:
            RangeIndex
        Columns:
            Name: t, dtype: datetime64[ns]
                Timestamp of the initial foot impact
            Name: contact_time, dtype: float64
                Time between final contact and initial contact
            Name: step_duration, dtype: float64
                Time between initial contact and the initial contact of the opposite foot
            Name: cadence, dtype: float64
                Steps per minute, derived from step_duration
            Name: stride_duration, dtype: float64
                Time between two initial contacts of the same foot
            Name: flight_ratio, dtype: float64
                The ratio of a step that both feet are in the air
            Name: impact, dtype: float64
                The peak acceleration at contact
    list
        A list of initial contact times
    list
        A list of final contact times

    """
    log.debug(
        "[ Extracting gait features from the vertical acceleration of a motion sensor"
    )

    from scipy.signal import find_peaks

    fc_peaks, _ = find_peaks(a_vert, prominence=1.5)
    ic_peaks, _ = find_peaks(-a_vert, prominence=1.5)

    log.debug("Finding initial and final contact peaks")
    ic_times_ns = timestamps.iloc[ic_peaks]
    fc_times_ns = timestamps.iloc[fc_peaks]
    log.debug("Found {} IC and {} FC peaks".format(len(ic_times_ns), len(fc_times_ns)))

    ic_times = pd.to_datetime(ic_times_ns)
    fc_times = pd.to_datetime(fc_times_ns)

    min_contact_time = pd.Timedelta(contact_time_range[0], "ms")
    max_contact_time = pd.Timedelta(contact_time_range[1], "ms")
    min_step_time = pd.Timedelta(step_time_range[0], "ms")
    max_step_time = pd.Timedelta(step_time_range[1], "ms")

    ds_ic = pd.DataFrame(
        {
            "t": ic_times,
            "t_contact_min": ic_times + min_contact_time,
            "t_step_min": ic_times + min_step_time,
            "t_ic": ic_times_ns,
            "impact": -a_vert.iloc[ic_peaks],
        }
    ).reset_index(drop=True)
    ds_fc = pd.DataFrame({"t": fc_times, "t_fc": fc_times_ns}).reset_index(drop=True)

    log.debug("Collecting contact pairs for feature extraction")
    # collect intitial-final contact pair
    df = pd.merge_asof(
        ds_ic,
        ds_fc,
        left_on="t_contact_min",
        right_on="t",
        direction="forward",
        suffixes=[None, "_fcm"],
        tolerance=max_contact_time - min_contact_time,
    )
    df["contact_time"] = (df["t_fc"] - df["t_ic"]) / 1e6
    df.drop(["t_fc", "t_fcm"], axis=1, inplace=True)

    # collect initial contact one foot and opposite foot
    df = pd.merge_asof(
        df,
        ds_ic[["t", "t_ic"]],
        left_on="t_step_min",
        right_on="t",
        suffixes=[None, "_opp"],
        direction="forward",
        tolerance=max_step_time - min_step_time,
    )
    df["step_duration"] = (df["t_ic_opp"] - df["t_ic"]) / 1e6
    df["cadence"] = 60 / df["step_duration"]

    # filter out invalid steps due to double ic/fc detections
    df = df[
        df["t"].shift(-1) - df["t"] > min_step_time
    ]  # double ic's lead to invalid step times
    df = df[
        df["step_duration"] > df["contact_time"]
    ]  # contact time cannot be longer than step time

    df["stride_duration"] = pd.to_numeric(df["t"].shift(-2) - df["t"]) / 1e6
    df = df[df["stride_duration"] > 0]  # stride duration must be positive
    df = df[
        df["t"].shift(-2) - df["t"] < 2 * max_step_time
    ]  # also enforce maximum stride time

    df["flight_ratio"] = (df["step_duration"] - df["contact_time"]) / df[
        "step_duration"
    ]

    # drop extra columns and do clean up
    df.drop(
        ["t_contact_min", "t_step_min", "t_ic", "t_opp", "t_ic_opp"],
        axis=1,
        inplace=True,
    )
    df.reset_index(drop=True, inplace=True)

    log.debug("] Done, returning {} gait cycles".format(len(df)))

    return df, ic_times, fc_times


def gait_symmety_index_from_acceleration(
    ax, ay, az, maxlag=150, deadlag=50, sample_rate=100
):
    """
    Determine the gait symmetry index (GSI) from the 3-axes acceleration.
    GSI computation from: "Gait Symmetry Assessment with a Low Back 3D
    Accelerometer in Post-Stroke Patients" (Zhang, 2018)

    Parameters
    ----------
    ax, ay, az : list
        List of the three axes of acceleration, direction is not important but should not change
        within a single computation
    maxlag : float
        Maximum lag to compute the autocorrelation and expect a peak. Units is in samples.
    deadlag : float
        Minimum lag to compute the autocorrelation and expect a peak. Units is in samples.
    sample_rate : float
        Expected sampling rate of the data

    Returns
    -------
    float
        The complement of the gsi, meaning 0 = symmetric, 1 = asymmetric
    float
        Lag corresponding to the stride duration (in seconds)
    """

    if len(ax) <= deadlag:
        return np.nan, np.nan

    # design 2nd order lp-butterworth filter
    from scipy import signal

    sos = signal.butter(2, 10, "low", fs=sample_rate, output="sos")
    fax = signal.sosfilt(sos, ax)
    fay = signal.sosfilt(sos, ay)
    faz = signal.sosfilt(sos, az)

    # use the unbiased autocorrelation (does not taper) to get unbiased value
    ARx = autocorrelate(fax)[:maxlag]
    ARy = autocorrelate(fay)[:maxlag]
    ARz = autocorrelate(faz)[:maxlag]
    Cstep = np.sqrt(ARx ** 2 + ARy ** 2 + ARz ** 2)

    # use biased autocorrelation (tapers off) to ensure getting the first peak
    ARx = autocorrelate(fax, unbiased=False)[:maxlag]
    ARy = autocorrelate(fay, unbiased=False)[:maxlag]
    ARz = autocorrelate(faz, unbiased=False)[:maxlag]

    ARx[ARx < 0] = 0
    ARy[ARy < 0] = 0
    ARz[ARz < 0] = 0
    Cstride = ARx + ARy + ARz
    Tstride = deadlag + np.argmax(Cstride[deadlag:])
    GSI = Cstep[Tstride // 2] / np.sqrt(3)

    stride_duration = Tstride / sample_rate

    return 1 - GSI, stride_duration
