import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os

import logging

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger("mergait-MusicLibary")


class MusicLibrary:
    """
    Class that manages the project's local music library, which mirrors the features and
    audio analysis of the Spotify API.
    """

    def __init__(self, data_path):
        self.df_tracks = pd.DataFrame([])
        self.df_features = pd.DataFrame([])
        self.df_analysis = pd.DataFrame([])
        self.df_sections = pd.DataFrame([])
        self.df_segments = pd.DataFrame([])
        self.df_artists = pd.DataFrame([])
        self.spotipy = None
        self.data_path = data_path

    def setSpotify(self, client_id, client_secret):
        """
        Sets the client id and secret for accessing the Spotify API. This is only required if new
        track information needs to be collected.

        Parameters
        ----------
        client_id : str
            Client id for the Spotify API
        client_secret : str
            Client secret for the Spotify API

        """
        client_credentials_manager = SpotifyClientCredentials(
            client_id=client_id, client_secret=client_secret
        )

        self.spotipy = spotipy.Spotify(
            client_credentials_manager=client_credentials_manager, requests_timeout=60
        )

    def load(self):
        """
        Load current state from disk
        """
        self.df_tracks = self.__load_from_disk("tracks.csv")
        self.df_features = self.__load_from_disk("features.csv")
        self.df_analysis = self.__load_from_disk("analysis.csv")
        self.df_sections = self.__load_from_disk("sections.csv")
        self.df_segments = self.__load_from_disk("segments.csv")
        self.df_artists = self.__load_from_disk("artists.csv")

        # should not make a difference but to keep the library clean
        # we cannot do this on save because nested objects cannot be compared easily
        self.df_tracks.drop_duplicates(inplace=True)
        self.df_features.drop_duplicates(inplace=True)
        self.df_analysis.drop_duplicates(inplace=True)
        self.df_sections.drop_duplicates(inplace=True)
        self.df_segments.drop_duplicates(inplace=True)
        self.df_artists.drop_duplicates(inplace=True)

    def save(self):
        """
        Save current state to disk
        """
        self.__save_to_disk(self.df_tracks, "tracks.csv")
        self.__save_to_disk(self.df_features, "features.csv")
        self.__save_to_disk(self.df_analysis, "analysis.csv")
        self.__save_to_disk(self.df_sections, "sections.csv")
        self.__save_to_disk(self.df_segments, "segments.csv")
        self.__save_to_disk(self.df_artists, "artists.csv")

    def getDataFrames(self):
        """
        Returns all DataFrames with library data.


        Returns
        -------
        pandas.DataFrame
            Contains general track data
        pandas.DataFrame
            Contains basic audio features per track
        pandas.DataFrame
            Contains in-depth audio analysis per track
        pandas.DataFrame
            Contains section boundaries and features (from audio analysis)
        pandas.DataFrame
            Contains segment pitch and timbre information (from audio analysis)
        pandas.DataFrame
            Contains artist information
        """
        return (
            self.df_tracks,
            self.df_features,
            self.df_analysis,
            self.df_sections,
            self.df_segments,
            self.df_artists,
        )

    def require_tracks(self, track_uris):
        """
        Ensure that the data of the given tracks are stored in the local music library, so
        that the data can be used in further analysis of the running data.

        Notes:
        - remember to load the libary with the load method, and call save afterwards to
        store the current state to disk.
        - new track information is collected using the Spotify API, thuis requires the client id
        and secret to be set with `setSpotify(client_id, client_secret)`.

        Parameters
        ----------
        track_uris : list[str]
            A list of track uris of the Spotify API

        """

        # find songs that are not in the feature database
        known_uris = (
            [] if len(self.df_tracks) == 0 else set(self.df_tracks["track_uri"].values)
        )
        required_uris = set(track_uris)
        unknown_uris = required_uris.difference(known_uris)

        self.__spotify_tracks(unknown_uris)

    def __spotify_tracks(self, track_uris):
        """
        Collect all Spotify API data related to given tracks, so that the local
        music library is up to date, requires the client id and secret has been
        set with `setSpotify(client_id, client_secret)`.

        Parameters
        ----------
        track_uris : list[str]
            A list of track uris of the Spotify API
        """

        # filter invalid ids
        track_uris = [i for i in track_uris if i and i != ""]

        if len(track_uris) == 0:
            return

        if self.spotipy is None:
            return

        # get track information (for album cover art)
        track_dict = self.spotipy.tracks(track_uris)
        # get audio features
        features_dict = self.spotipy.audio_features(track_uris)

        # remove None values from features lists
        track_dict["tracks"] = [i for i in track_dict["tracks"] if i]
        features_dict = [i for i in features_dict if i]

        df_tracks = pd.json_normalize(track_dict["tracks"], sep="_")
        df_tracks.rename({"uri": "track_uri"}, axis=1, inplace=True)
        self.df_tracks = self.df_tracks.append(df_tracks)

        df_features = pd.DataFrame(features_dict)
        df_features.rename({"uri": "track_uri"}, axis=1, inplace=True)
        self.df_features = self.df_features.append(df_features)

        for track_info in track_dict["tracks"]:
            analysis_dict = self.spotipy.audio_analysis(track_info["uri"])
            df_analysis = pd.json_normalize(analysis_dict, sep="_")
            df_analysis["track_uri"] = track_info["uri"]
            self.df_analysis = self.df_analysis.append(df_analysis)

            df_sections = pd.DataFrame(df_analysis.sections[0])
            df_sections["track_uri"] = track_info["uri"]
            df_sections.reset_index(inplace=True)
            df_sections.rename(columns={"index": "section"}, inplace=True)
            self.df_sections = self.df_sections.append(df_sections)

            df_segments = pd.DataFrame(df_analysis.segments[0])
            df_segments["track_uri"] = track_info["uri"]
            df_segments.reset_index(inplace=True)
            df_segments.rename(columns={"index": "segment"}, inplace=True)
            self.df_segments = self.df_segments.append(df_segments)

            artist_uri = track_info["artists"][0]["uri"]
            if (
                len(self.df_artists) == 0
                or artist_uri not in self.df_artists["artist_uri"]
            ):
                artist_dict = self.spotipy.artist(artist_uri)
                df_artists = pd.json_normalize(artist_dict, sep="_")
                df_artists.rename({"uri": "artist_uri"}, axis=1, inplace=True)
                self.df_artists = self.df_artists.append(df_artists)

    def __load_from_disk(self, fname):
        if os.path.exists(self.data_path + fname):
            df = pd.read_csv(self.data_path + fname)
        else:
            df = pd.DataFrame([])
        return df

    def __save_to_disk(self, df, fname):
        df.to_csv(self.data_path + fname, index=False)
