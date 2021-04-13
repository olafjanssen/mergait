Module mergait.rawreader
========================

Classes
-------

`RawReader()`
:   Reads and consumes raw data files (stored as raw.jsonl) from the Music Enabled Running project.
    
    The state can be updated by feeding it additional lines (msg) from the data file.
    You can then extract the data of the different sensors and modalities as Pandas dataframes.

    ### Methods

    `get_footpods_df(self)`
    :   Get per-step data of (RunScribe) footpods in a Pandas DataFrame.
        
        Returns
        -------
        pandas.DataFrame
            Pandas dataframe with all the per-step data of both left and right footpod
        
            Columns:
        
                Name: t, dtype: datetime64[ns]
                    Timestamp [s] of sensor event, not the exact step timestamp
        
                Name: foot, dtype: object
                    Foot for pod 'left' or 'right'
        
                Name: pronation, dtype: float64
                    Maximum foot pronation [deg]. Is expected to be a negative value.
        
                Name: braking, dtype: float64
                    Braking force on foot on impact [G]
        
                Name: impact, dtype: float64
                    Downward maximal foot impact [G]
        
                Name: contact_time, dtype: int64
                    Time between initial contact and final contact of foot [ms]
        
                Name: flight_ratio, dtype: float64
                    Ratio between time that foot is in the air to the total stride duration.
        
                Name: strike, dtype: int64
                    Initial strike contact of the foot, 1=heel, 15=toe
        
                Name: power, dtype: int64
                    Power of the step [W]

    `get_footpods_sc_df(self)`
    :   Get speed-cadence sensor data of (RunScribe) footpods per foot in a Pandas DataFrame.
        The data is not per-step but with a sampling frequency of about 1Hz.
        
        Returns
        -------
        pandas.DataFrame
            Pandas dataframe with speed-cadence data of both left and right footpod
        
            Columns:
        
                Name: t, dtype: datetime64[ns]
                    Timestamp [s] of sensor event
        
                Name: foot, dtype: object
                    Foot for pod 'left' or 'right'
        
                Name: cadence, dtype: int64
                    Strides per minute [/min]. This is about half the step frequency
        
                Name: speed, dtype: float64
                    Average speed of the foot [m/s] based on estimated user height (may not be set properly)

    `get_music_df(self)`
    :   Get information about the state of the (Spotify) music player in a Pandas DataFrame.
        
        Returns
        -------
        pandas.DataFrame
            Pandas dataframe with music player data.
        
            Columns:
        
                Name: t, dtype: datetime64[ns]
                    Timestamp [s] of sensor event
        
                Name: track_uri, dtype: object
                    URI of the track being played
        
                Name: paused, dtype: bool
                    Whether the player is playing or on pause
        
                Name: artist, dtype: object
                    String of the artist name
        
                Name: track, dtype: object
                    String of the track title
        
                Name: context_uri, dtype: object
                    URI of the track context, usually a playlist
        
                Name: context, dtype: object
                    String of the track context, usually a playlist
        
                Name: position, dtype: int64
                    Position [s] of the playhead in the track
        
                Name: repeat_mode, dtype: object
                    State of the repeat mode, 'off', 'track', 'context'
        
                Name: shuffle, dtype: bool
                    State of the shuffle option
        
                Name: crossfade, dtype: bool
                    State indicating whether crossfade is turned on

    `get_phone_activity_df(self)`
    :   Get (i)Phone activity and pedometer related data in a Pandas DataFrame.
        
        Returns
        -------
        pandas.DataFrame
            Pandas dataframe with activity and pedometer data.
        
            Columns:
        
                Name: t, dtype: datetime64[ns]
                    Timestamp [s] of sensor event
        
                Name: activity, dtype: object
                    Detected activity 'stationary', 'walking', 'running'
        
                Name: speed, dtype: float64
                    Speed of phone motion [m/s]
        
                Name: step, dtype: float64
                    Number of steps taken since starting session
        
                Name: cadence, dtype: int64
                    Step frequency [/min]
        
                Name: floors_ascended, dtype: int64
                    Number of floors ascended since starting session
        
                Name: floors_descended, dtype: int64
                    Number of floors descended since starting session

    `get_phone_location_df(self)`
    :   Get GPS location data of the phone. Update frequency may vary.
        
        Returns
        -------
        pandas.DataFrame
            Pandas dataframe with GPS data.
        
            Columns:
        
                Name: t, dtype: datetime64[ns]
                    Timestamp [s] of sensor event
        
                Name: lon, dtype: float64
                    Longitude [deg]
        
                Name: lat, dtype: float64
                    Latitude [deg]
        
                Name: lonlat_acc, dtype: float64
                    Estimated horizontal accuracy of longitude and latitude [deg]
        
                Name: alt, dtype: float64
                    Altitude [m]
        
                Name: alt_acc, dtype: float64
                    Estimated vertical accuracy of altitude [deg]
        
                Name: course, dtype: float64
                    Heading course in horizontal plane [deg]
        
                Name: alt_acc, dtype: float64
                    Estimated course accuracy [deg]
        
                Name: speed, dtype: float64
                    Speed of sensor [m/s]
        
                Name: speed_acc, dtype: float64
                    Estimated accuracy of speed [m/s]

    `get_phone_motion_df(self)`
    :   Get motion data of the IMU sensor of the (i)Phone in a Pandas DataFrame.
        For the iPhone the data is sampled at 100Hz.
        
        Returns
        -------
        pandas.DataFrame
            Pandas dataframe with real-time IMU data
        
            Columns:
        
                Name: t, dtype: datetime64[ns]
                    Timestamp [s] of sensor event
        
                Name: ax, dtype: float64
                    Acceleration (including gravity) in the x-direction [G]
        
                Name: ay, dtype: float64
                    Acceleration (including gravity) in the y-direction [G]
        
                Name: az, dtype: float64
                    Acceleration (including gravity) in the z-direction [G]
        
                Name: gx, dtype: float64
                    Gravity acceleration in the x-direction [G]
        
                Name: gy, dtype: float64
                    Gravity acceleration in the y-direction [G]
        
                Name: gz, dtype: float64
                    Gravity acceleration in the z-direction [G]
        
                Name: a_vert, dtype: float64
                    Acceleration in vertical direction [G], this is inner product of a and g
        
                Name: rx, dtype: float64
                    Rotation velocity [deg/s] in x-direction
        
                Name: ry, dtype: float64
                    Rotation velocity [deg/s] in y-direction
        
                Name: rz, dtype: float64
                    Rotation velocity [deg/s] in z-direction

    `get_timestamp_range(self)`
    :   Get the minimum and maximum timestamp values in the data.
        
        Returns
        -------
        list: integer
            Minimum and maximum value of the timestamp in the data

    `update_with(self, msg)`
    :   Updates the class state with a new message from the raw data file.
        
        Parameters
        ----------
        msg : dict
            The dictionary representing the data message from the raw file.
            Note, the raw JSON line must be first converted to a dict.