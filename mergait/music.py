""" Music parameter related utility functions

These functions help merge music related data with other datasets
"""

import pandas as pd
import numpy as np
from mergait.bouts import *


def merge_music_playstate(df, df_music, columns=["t", "track_uri"]):
    """
    Merge music playstate information into another dataset.
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
    """

    df = df.copy()

    # tracks may occur multiple times in the dataset, so we group not per track but per track-boundary
    df_music = pd.DataFrame(df_music)
    df_music["__temp"] = (df_music.track_uri != df_music.track_uri.shift()).cumsum()
    df_music_songs = df_music.groupby(by=["__temp"], sort=False)

    # merge simple properties, making sure track_uri remains categorical
    df = pd.merge_asof(
        df, df_music[["t", "track_uri"]].dropna(), on="t", direction="backward"
    )

    # for the playhead position we must interpolate the data, except for when the playstate is paused
    keys = list(df_music_songs.groups.keys())
    for idx in range(len(df_music_songs)):
        is_last = idx + 1 == len(df_music_songs)

        song = df_music_songs.get_group(keys[idx])
        next_song = False if is_last else df_music_songs.get_group(keys[idx + 1])

        song_valid = song["paused"]
        song_bouts = extract_bouts(song, song_valid, keep_invalid=True)

        # pad last bout to the beginning of next song, so remember the last state until song finishes
        if is_last:
            song_bouts.tail(1).t_end = df.t.max()
        else:
            song_bouts.tail(1).t_end = next_song.t.iloc[0]

        # add filter for when there is no music yet, or music is paused
        add_bouts_as_column(df, song_bouts, new_column="bad_no_music", reset_value=True)
        # interpolate and extrapolate play position
        interpolate_bouts_as_column(
            df, song, song_bouts, new_column="position", value_column="position"
        )

    # remove playstate position when no music is playing
    if not "bad_no_music" in df:
        df["bad_no_music"] = True
    if not "position" in df:
        df["position"] = pd.Series()

    df.loc[df["bad_no_music"] == True, "position"] = np.nan

    return df


def append_music_section(
    df, df_sections, timestamp_column="t", position_column="position"
):
    """
    Appends the section index of the track to the data, using the playstate position and
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
    """
    df = df.copy()

    df = pd.merge_asof(
        df.sort_values(by="position"),
        df_sections[["track_uri", "start", "section"]].sort_values(by="start"),
        left_on="position",
        right_on="start",
        left_by=["track_uri"],
        right_by="track_uri",
        direction="backward",
    )
    df.drop(["start"], axis=1, inplace=True)

    return df.sort_values(by=timestamp_column).reset_index(drop=True)


def get_music_features_per_section(
    df_features, df_sections, df_segments, track_uris=None
):
    """
    Obtain the music features per section of a track.
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
    """
    if track_uris is None:
        df = df_sections
    else:
        df = df_sections[df_sections["track_uri"].isin(track_uris)]

    df = df.merge(df_features, on="track_uri", suffixes=[None, "_track"])
    df.drop(["type", "id", "track_href", "analysis_url"], axis=1, inplace=True)
    df.sort_values(by="start", inplace=True)

    # add segment, pitch and timbre information
    df_segs = df_segments[df_segments["track_uri"].isin(df["track_uri"])].sort_values(
        by="start"
    )
    df = pd.merge_asof(
        df_segs[["track_uri", "start", "pitches", "timbre"]],
        df,
        on="start",
        by="track_uri",
        suffixes=["_segment", None],
        direction="backward",
    )

    import ast

    def mean(a):
        c = np.array([ast.literal_eval(item) for item in a.values]).flatten()
        return np.mean(c)

    def std(a):
        c = np.array([ast.literal_eval(item) for item in a.values]).flatten()
        return np.std(c)

    agg_funs = {key: "first" for key in df.columns}
    agg_funs["pitches"] = [mean, std]
    agg_funs["timbre"] = [mean, std]

    df = df.groupby(["track_uri", "section"]).agg(agg_funs)
    df.columns = df.columns.map(lambda x: "_".join(a for a in x if a != "first"))

    df.rename(
        columns={
            "confidence": "duration_confidence",
            "duration_mw": "duration_track_ms",
        },
        inplace=True,
    )

    df.reset_index(drop=True, inplace=True)

    return df


def get_music_features_per_track(df_features, df_segments, track_uris=None):
    """
    Obtain the music features per track.
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
    """
    if track_uris is None:
        df = df_features
    else:
        df = df_features[df_features["track_uri"].isin(track_uris)]

    df.drop(["type", "id", "track_href", "analysis_url"], axis=1, inplace=True)

    # add segment, pitch and timbre information
    df_segs = df_segments[df_segments["track_uri"].isin(df["track_uri"])]
    df = df_segs[["track_uri", "pitches", "timbre"]].merge(
        df, on="track_uri", suffixes=["_segment", None]
    )

    import ast

    def mean(a):
        c = np.array([ast.literal_eval(item) for item in a.values]).flatten()
        return np.mean(c)

    def std(a):
        c = np.array([ast.literal_eval(item) for item in a.values]).flatten()
        return np.std(c)

    agg_funs = {key: "first" for key in df.columns}
    agg_funs["pitches"] = [mean, std]
    agg_funs["timbre"] = [mean, std]

    df = df.groupby(["track_uri"]).agg(agg_funs)
    df.columns = df.columns.map(lambda x: "_".join(a for a in x if a != "first"))
    df.reset_index(drop=True, inplace=True)

    return df


def get_music_track_info(df_tracks, df_artists, track_uris):
    """
    Get human readable general track info used for debugging and displaying purposes.
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
    """
    import ast

    if track_uris is None:
        df = df_tracks
    else:
        df = df_tracks[df_tracks["track_uri"].isin(track_uris)]

        df["artist_uri"] = df["artists"].transform(
            lambda x: ast.literal_eval(x)[0]["uri"]
        )
        df["artists"] = df["artists"].transform(
            lambda x: ast.literal_eval(x)[0]["name"]
        )
        df["album_images"] = df["album_images"].transform(
            lambda x: ast.literal_eval(x)[0]["url"]
        )

        df = df[
            [
                "artists",
                "artist_uri",
                "name",
                "popularity",
                "album_name",
                "album_uri",
                "album_images",
            ]
        ]
        df.rename(
            columns={"artists": "artist_name", "album_images": "cover_url"},
            inplace=True,
        )

        df = df.merge(
            df_artists[["artist_uri", "popularity", "genres", "followers_total"]],
            left_on="artist_uri",
            right_on="artist_uri",
            suffixes=[None, "_artist"],
            how="left",
        )
        df.drop_duplicates(inplace=True)
        df.reset_index(drop=True, inplace=True)
    return df
