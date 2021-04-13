Module mergait.music
====================
Music parameter related utility functions

These functions help merge music related data with other datasets

Functions
---------

    
`append_music_section(df, df_sections, timestamp_column='t', position_column='position')`
:   Appends the section index of the track to the data, using the playstate position and
    the section boundaries.
    
    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame containing the data the music section must be appended to
    df_sections : pandas.Dataframe
        The DataFrame containing music section boundaries per track
    timestamp_column : str
        The column containing the timestamp (for sorting)
    position_column : str
        The column containing the playstate position (in ms)
    
    Returns
    -------
    pandas.DataFrame
        A new DataFrame with the appended music section index

    
`get_music_features_per_section(df_features, df_sections, df_segments, track_uris=None)`
:   Obtain the music features per section of a track.
    As input, the pandas DataFrames resulting from the MusicLibrary class are required.
    
    Parameters
    ----------
    df_features : pandas.Dataframe
        Contains the basic track features
    df_sections : pandas.Dataframe
        Contains the section boundaries per track
    df_segments : pandas.Dataframe
        Contains sections with pitch and timbre information
    track_uris : list
        Optional list of tracks to get the data for, if None get all features
    
    Returns
    -------
    pandas.DataFrame
        For information about the columns, consult the Spotify API documentation

    
`get_music_features_per_track(df_features, df_segments, track_uris=None)`
:   Obtain the music features per track.
    As input, the pandas DataFrames resulting from the MusicLibrary class are required.
    
    Parameters
    ----------
    df_features : pandas.Dataframe
        Contains the basic track features
    df_segments : pandas.Dataframe
        Contains sections with pitch and timbre information
    track_uris : list
        Optional list of tracks to get the data for, if None get all features
    
    Returns
    -------
    pandas.DataFrame
        For information about the columns, consult the Spotify API documentation

    
`get_music_track_info(df_tracks, df_artists, track_uris)`
:   Get human readable general track info used for debugging and displaying purposes.
    As input, the pandas DataFrames resulting from the MusicLibrary class are required.
    
    Parameters
    ----------
    df_tracks : pandas.Dataframe
        Contains general track information
    df_artists : pandas.Dataframe
        Contains artist information
    track_uris : list
        Optional list of tracks to get the data for, if None get all features
    
    Returns
    -------
    pandas.DataFrame
        For information about the columns, consult the Spotify API documentation

    
`merge_music_playstate(df, df_music, columns=['t', 'track_uri'])`
:   Merge music playstate information into another dataset.
    1) Given columns are appended by a backward merge on time
    2) The playstate position is interpolated when the music is playing
    3) A filter column is added to indicate whether music is playing
    
    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame containing the data is merged with music playstate data
    df_music : pandas.Dataframe
        The DataFrame containing music playstate
    columns : list[str]
        The columns of the music DataFrame that are merged backward into df
    
    Returns
    -------
    pandas.DataFrame
        A new DataFrame with the interpolated music playstate merged into it