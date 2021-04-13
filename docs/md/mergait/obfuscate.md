Module mergait.obfuscate
========================
Data obfuscation methods

These functions are intended to help obfuscate the internal data for the purpose of anonymization.

Note that most of the methods assume the data is for a single user, because most data analysis is 
performed on a per user basis. Only the sessions method will encode the internal user ids. It is 
then your responsibility to apply this transformation when combining data from multiple users.

Functions
---------

    
`obfuscate_by_timestamp_offset(dfs, time_offset, range_column='t')`
:   Obfuscating timestamps by using a time offset. Most commonly the time offset is
    obtained from the `obfuscate_sessions` method and applied to all other DataFrames
    with timestamp information.
    
    Parameters
    ----------
    dfs : list
        List of DataFrames containing timestamp information
    time_offset : pd.TimeDelta
        A timeoffset to apply to all given DataFrames
    range_column : str
        Column name for the timestamp
    
    Returns
    -------
    list
        The list of time-shifted DataFrames

    
`obfuscate_location(df_location, level=3)`
:   Obfuscating (gps) location data for data exports at different levels of anonymity.
    
    Parameters
    ----------
    df_location : pandas.DataFrame
        DataFrame containing location data
    level : Obfuscate
        Level of obfuscation,
        * >=BASIC removes direct location data (lon, lat)
        * >=FULL also removes indirect location data (course/heading and altitude)
    
    Returns
    -------
    pandas.DataFrame
        The obfuscated location DataFrame

    
`obfuscate_music(df_music, df_music_features, level=3)`
:   Obfuscating third-party identifiers (e.g. Spotify) in music related data.
    
    Parameters
    ----------
    df_music : pandas.DataFrame
        DataFrame containing music information with third-party (track) ids
    df_music_features : list
        List of DataFrames containing music features linked to the same track ids
    
    level : Obfuscate
        Level of obfuscation,
        * >=BASIC replaces track and playlist (context) ids by integer index, also
            removes human-readable fields such as track title and artist name
    
    Returns
    -------
    pandas.DataFrame
        The obfuscated music DataFrame
    list
        The list of music feature DataFrames
    sklearn.preprocessing.LabelEncoder
        The encoder for track ids
    sklearn.preprocessing.LabelEncoder
        The encoder for context ids

    
`obfuscate_sessions(df_sessions, level=3)`
:   Obfuscating session data for data exports at different levels of anonymity.
    
    Parameters
    ----------
    df_sessions : pandas.DataFrame
        DataFrame containing session data
    level : Obfuscate
        Level of obfuscation,
        * >=MIN replaces all internal identifiers by indexed value
        * >=BASIC shifts all session timestamps so that the first session of a user starts at t=0
    
    Returns
    -------
    pandas.DataFrame
        The obfuscated sessions DataFrame
    sklearn.preprocessing.LabelEncoder
        The encoder for session ids
    sklearn.preprocessing.LabelEncoder
        The encoder for user ids
    pandas.Series
        Timeoffset per user

Classes
-------

`Obfuscate()`
:   Enum class for indicating different levels of data obfuscation.
    Read the documentation of the individual obfuscation method on what happens at each level.

    ### Class variables

    `BASIC`
    :

    `FULL`
    :

    `MIN`
    :

    `NONE`
    :