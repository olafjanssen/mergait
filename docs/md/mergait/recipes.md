Module mergait.recipes
======================
High-level recipes for transforming raw data into statistics

Functions
---------

    
`compute_gsi_from_imu_recipe(df, df_imu, by=['track_uri', 'session_id', 'section'])`
:   Recipe for computing the gait symmetric index (GSI) from bouts of imu data.
    
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

    
`filter_to_valid_bouts_recipe(df, df_music, df_phone_activity, df_sessions, sections=None)`
:   Recipe for filtering valid running bouts per track or section.
    
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

    
`recipe_footpod_symmetry(df_footpods, df_music, df_phone_activity, df_sessions, sections=None)`
:   Recipe for extracting statistical symmetry information per song for
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

    
`recipe_imu_symmetry(df_imu, df_music, df_phone_activity, df_sessions, sections=None)`
:   Recipe for extracting statistical symmetry information per song for
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