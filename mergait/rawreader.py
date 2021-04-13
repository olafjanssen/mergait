import pandas as pd


class RawReader:
    """
    Reads and consumes raw data files (stored as raw.jsonl) from the Music Enabled Running project.

    The state can be updated by feeding it additional lines (msg) from the data file.
    You can then extract the data of the different sensors and modalities as Pandas dataframes.
    """

    def __init__(self):
        self.footpods = []
        self.footpods_sc = []
        self.phone_activity = []
        self.phone_motion = []
        self.music = []
        self.phone_location = []
        self.t_range = []

    def update_with(self, msg):
        """
        Updates the class state with a new message from the raw data file.

        Parameters
        ----------
        msg : dict
            The dictionary representing the data message from the raw file.
            Note, the raw JSON line must be first converted to a dict.

        """
        if "t" in msg:
            t = msg["t"]
            self.t_range = [t, t] if self.t_range == [] else [self.t_range[0], t]

        if msg["type"] == "iPhone-pedo":
            self.phone_activity.append(
                {
                    "t": pd.Timestamp(msg["t"], unit="s"),
                    "activity": msg["pedo"]["activity"],
                    "speed": 0
                    if msg["pedo"]["pace"] == 0
                    else 1.0 / msg["pedo"]["pace"],
                    "step": msg["pedo"]["step"],
                    "cadence": msg["pedo"]["cadence"] * 60,
                    "floors_ascended": msg["pedo"]["floorsAscended"]
                    if "floorsAscended" in msg["pedo"]
                    else 0,
                    "floors_descended": msg["pedo"]["floorsDescended"]
                    if "floorsDescended" in msg["pedo"]
                    else 0,
                }
            )

        if msg["type"] == "iPhone-motion":
            gx = msg["motion"]["ag"][0] - msg["motion"]["a"][0]
            gy = msg["motion"]["ag"][1] - msg["motion"]["a"][1]
            gz = msg["motion"]["ag"][2] - msg["motion"]["a"][2]
            a_vert = (
                msg["motion"]["a"][0] * gx
                + msg["motion"]["a"][1] * gy
                + msg["motion"]["a"][2] * gz
            )

            self.phone_motion.append(
                {
                    "t": pd.Timestamp(msg["t"], unit="s"),
                    "ax": msg["motion"]["a"][0],
                    "ay": msg["motion"]["a"][1],
                    "az": msg["motion"]["a"][2],
                    "gx": gx,
                    "gy": gy,
                    "gz": gz,
                    "a_vert": a_vert,
                    "rx": msg["motion"]["r"][0],
                    "ry": msg["motion"]["r"][1],
                    "rz": msg["motion"]["r"][2],
                }
            )

        if msg["type"] == "iPhone-location":
            self.phone_location.append(
                {
                    "t": pd.Timestamp(msg["location"]["timestamp"], unit="s"),
                    "lon": msg["location"]["coordinate"]["lon"],
                    "lat": msg["location"]["coordinate"]["lat"],
                    "lonlat_acc": msg["location"]["coordinate"]["acc"],
                    "alt": msg["location"]["altitude"]["val"],
                    "alt_acc": msg["location"]["altitude"]["acc"],
                    "course": msg["location"]["course"]["val"],
                    "course_acc": msg["location"]["course"]["acc"],
                    "speed": msg["location"]["speed"]["val"],
                    "speed_acc": msg["location"]["speed"]["acc"],
                }
            )

        if msg["type"] == "RunScribe-speedcadence":
            self.footpods_sc.append(
                {
                    "t": pd.Timestamp(msg["t"], unit="s"),
                    "foot": msg["runscribe"]["foot"],
                    "cadence": msg["rsc"]["cadence"],
                    "speed": msg["rsc"]["speed"],
                }
            )

        if msg["type"] == "RunScribe-metrics":
            self.footpods.append(
                {
                    "t": pd.Timestamp(msg["t"], unit="s"),
                    "foot": msg["runscribe"]["foot"],
                    "pronation": msg["metrics"]["pronation"],
                    "braking": msg["metrics"]["braking"],
                    "impact": msg["metrics"]["impact"],
                    "contact_time": msg["metrics"]["contactTime"],
                    "flight_ratio": msg["metrics"]["flightRatio"],
                    "strike": msg["metrics"]["strikeType"],
                    "power": msg["metrics"]["power"],
                }
            )

        if msg["type"] == "Spotify" and "playstate" in msg:

            if "name" in msg["playstate"]:
                split_track = msg["playstate"]["name"].split("-", 2)
                msg["playstate"]["artist"] = split_track[0].strip()
                msg["playstate"]["track"] = split_track[1].strip()

            self.music.append(
                {
                    "t": pd.Timestamp(msg["t"], unit="s"),
                    "track_uri": msg["playstate"]["uri"],
                    "paused": msg["playstate"]["paused"],
                    "artist": msg["playstate"]["artist"],
                    "track": msg["playstate"]["track"],
                    "context_uri": msg["playstate"]["contextUri"],
                    "context": msg["playstate"]["contextTitle"],
                    "position": msg["playstate"]["position"] / 1000,
                    "repeat_mode": msg["playstate"]["repeatMode"]
                    if "repeatMode" in msg
                    else "off",
                    "shuffle": msg["playstate"]["shuffle"]
                    if "shuffle" in msg
                    else False,
                    "crossfade": msg["playstate"]["crossfadeState"]
                    if "crossfadeState" in msg
                    else False,
                }
            )

        return True

    def get_footpods_df(self):
        """
        Get per-step data of (RunScribe) footpods in a Pandas DataFrame.

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

        """
        return pd.DataFrame(self.footpods)

    def get_footpods_sc_df(self):
        """
        Get speed-cadence sensor data of (RunScribe) footpods per foot in a Pandas DataFrame.
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

        """
        return pd.DataFrame(self.footpods_sc)

    def get_phone_motion_df(self):
        """
        Get motion data of the IMU sensor of the (i)Phone in a Pandas DataFrame.
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


        """
        return pd.DataFrame(self.phone_motion)

    def get_phone_location_df(self):
        """
        Get GPS location data of the phone. Update frequency may vary.

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

        """
        return pd.DataFrame(self.phone_location)

    def get_phone_activity_df(self):
        """
        Get (i)Phone activity and pedometer related data in a Pandas DataFrame.

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

        """
        return pd.DataFrame(self.phone_activity)

    def get_music_df(self):
        """
        Get information about the state of the (Spotify) music player in a Pandas DataFrame.

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

        """
        return pd.DataFrame(self.music)

    def get_timestamp_range(self):
        """
        Get the minimum and maximum timestamp values in the data.

        Returns
        -------
        list: integer
            Minimum and maximum value of the timestamp in the data

        """
        return self.t_range
