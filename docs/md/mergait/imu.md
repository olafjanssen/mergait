Module mergait.imu
==================
Methods that extract features from imu data.

Functions
---------

    
`gait_features_from_vertical_acceleration(timestamps, a_vert, contact_time_range=[50, 200], step_time_range=[200, 1000])`
:   Extract gait features from the vertical acceleration of a IMU alone.
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

    
`gait_symmety_index_from_acceleration(ax, ay, az, maxlag=150, deadlag=50, sample_rate=100)`
:   Determine the gait symmetry index (GSI) from the 3-axes acceleration.
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