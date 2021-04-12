""" Data obfuscation methods

These functions are intended to help obfuscate the internal data for the purpose of anonymization.

Note that most of the methods assume the data is for a single user, because most data analysis is 
performed on a per user basis. Only the sessions method will encode the internal user ids. It is 
then your responsibility to apply this transformation when combining data from multiple users.
"""

import pandas as pd


class Obfuscate:
    """
    Enum class for indicating different levels of data obfuscation.
    Read the documentation of the individual obfuscation method on what happens at each level.
    """

    NONE = 0
    MIN = 1
    BASIC = 2
    FULL = 3


def obfuscate_sessions(df_sessions, level=Obfuscate.FULL):
    """
    Obfuscating session data for data exports at different levels of anonymity.

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
    """
    from sklearn import preprocessing

    df_sessions = df_sessions.copy()

    if level >= Obfuscate.MIN:
        # convert internal session_id and user_id to a label
        session_le = preprocessing.LabelEncoder()
        user_le = preprocessing.LabelEncoder()

        df_sessions["session_id"] = session_le.fit_transform(df_sessions["session_id"])
        df_sessions["session_id"] = df_sessions["session_id"].transform(
            lambda x: "s" + str(x)
        )

        df_sessions["user_id"] = user_le.fit_transform(df_sessions["user_id"])
        df_sessions["user_id"] = df_sessions["user_id"].transform(
            lambda x: "u" + str(x)
        )

    # re-index time stamps
    time_offset = {}
    if level >= Obfuscate.BASIC:
        for idx, df_user in df_sessions.groupby("user_id"):
            time_offset[idx] = df_user["t_start"].values[0]

            df_sessions.loc[df_sessions.user_id == idx, "t_start"] -= pd.to_timedelta(
                pd.to_datetime(time_offset[idx]).value
            )
            df_sessions.loc[df_sessions.user_id == idx, "t_end"] -= pd.to_timedelta(
                pd.to_datetime(time_offset[idx]).value
            )

    return df_sessions, session_le, user_le, pd.Series(time_offset)


def obfuscate_location(df_location, level=Obfuscate.FULL):
    """
    Obfuscating (gps) location data for data exports at different levels of anonymity.

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
    """
    df_location = df_location.copy()

    # remove location information
    if level >= Obfuscate.BASIC:
        df_location[["lon", "lat"]] = None

    if level >= Obfuscate.FULL:
        df_location[["course", "alt"]] = None

    return df_location


def obfuscate_music(df_music, df_music_features, level=Obfuscate.FULL):
    """
    Obfuscating third-party identifiers (e.g. Spotify) in music related data.

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
    """
    from sklearn import preprocessing

    df_music = df_music.copy()
    df_music_features = [dfm.copy() for dfm in df_music_features]

    # remove Spotify metadata
    if level >= Obfuscate.BASIC:
        # convert uris to a label
        track_le = preprocessing.LabelEncoder()
        context_le = preprocessing.LabelEncoder()

        tracks = df_music["track_uri"].values
        df_music["track_uri"] = track_le.fit_transform(df_music["track_uri"])
        df_music["track_uri"] = df_music["track_uri"].transform(lambda x: "t" + str(x))

        df_music["context_uri"] = context_le.fit_transform(df_music["context_uri"])
        df_music["context_uri"] = df_music["context_uri"].transform(
            lambda x: "c" + str(x)
        )

        # remove human readable track identity information
        df_music[["artist", "track", "context"]] = None

        # propagate new ids to the feature DataFrames
        df_obfuscated_features = []
        for dfm in df_music_features:
            dfm = dfm[dfm["track_uri"].isin(tracks)]
            dfm["track_uri"] = track_le.transform(dfm["track_uri"])
            dfm["track_uri"] = dfm["track_uri"].transform(lambda x: "t" + str(x))

            df_obfuscated_features.append(dfm)

    return df_music, df_obfuscated_features, track_le, context_le


def obfuscate_by_timestamp_offset(dfs, time_offset, range_column="t"):
    """
    Obfuscating timestamps by using a time offset. Most commonly the time offset is
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
    """
    df_obf = []

    for df in dfs:
        df = df.copy()
        df.t -= pd.to_timedelta(time_offset.value)
        df_obf.append(df)

    return df_obf
