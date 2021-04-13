# Codebook
This codebook or data dictionary describes the columns of the dataframes this package handles.

## footpods.csv
Per-step data of both left and right footpod.

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

## footpods_sc.csv

Speed-cadence sensor data of (RunScribe) footpods per foot. The data is not per-step but with a sampling frequency of about 1Hz.

    Name: t, dtype: datetime64[ns]
        Timestamp [s] of sensor event

    Name: foot, dtype: object
        Foot for pod 'left' or 'right'

    Name: cadence, dtype: int64
        Strides per minute [/min]. This is about half the step frequency

    Name: speed, dtype: float64
        Average speed of the foot [m/s] based on estimated user height (may not be set properly)


## phone_motion.csv(.gz)
Real-time motion data of the IMU sensor of the (i)Phone. For the iPhone the data is sampled at 100Hz.

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

## phone_location.csv

(GPS) location data of the phone. Update frequency may vary.

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

## phone_activity.csv
Data from the phone activity center and pedometer.

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

## music.csv
Information about the state of the (Spotify) music player during a run.

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

## music_features_tracks.csv

    Name: track_uri, dtype: object
        URI of the track being played

    Name: duration_ms, dtype: int
        Duration of the music track [ms]

    Name: pitches_mean, dtype: float64
        Average value of all the pitches

    Name: pitches_std, dtype: float64
        Standard deviation of the pitches

    Name: timbre_mean, dtype: float64
        Average value of all the timbre values 

    Name: timbre_std, dtype: float64
        Standard deviation of the timbre values

    Name: tempo, dtype: float64
        Average tempo of the track [bpm]

    Name: key, dtype: int
        Musical key [0 = C, 1 = C#, 2 = D, etc]

    Name: mode, dtype: int
        Musical modality, or scale [0 = Minor, 1 = Major]

    Name: time_signature, dtype: int
        The time signtature given in beats per measure

    Name: danceability, dtype: float64
        Value indicating the amount of danceability, between 0.0 - 1.0

    Name: speechiness, dtype: float64
        Value indicating the confidence of being a speech work instead of music, between 0.0 - 1.0

    Name: acousticness, dtype: float64
        Value indicating the amount of acousticness, between 0.0 - 1.0

    Name: instrumentalness, dtype: float64
        Value indicating the confidence of being an instrumental track, between 0.0 - 1.0

    Name: liveness, dtype: float64
        Value indicating the confidence of being a live performance, between 0.0 - 1.0

    Name: energy, dtype: float64
        Value indicating the amount of emotional energy, between 0.0 - 1.0

    Name: valence, dtype: float64
        Value indicating the amount of musical positivity, between 0.0 - 1.0

    Name: loudness, dtype: float64
        Average loudness [dB]


## music_features_sections.csv

    Name: track_uri, dtype: object
        URI of the track being played

    Name: start, dtype: float64
        Start of the music section [s]

    Name: section, dtype: int
        Index of the section within a song (0-based)

    Name: duration, dtype: float64
        Duration of the section [s]

    Name: duration_confidence, dtype: float64
        Confidence indication of the section duration

    Name: duration_track_ms, dtype: int
        Duration of the music track [ms]

    Name: pitches_mean, dtype: float64
        Average value of all the pitches within a section

    Name: pitches_std, dtype: float64
        Standard deviation of the pitches within a section

    Name: timbre_mean, dtype: float64
        Average value of all the timbre values within a section

    Name: timbre_std, dtype: float64
        Standard deviation of the timbre values within a section

    Name: tempo, dtype: float64
        Tempo of the section [bpm]

    Name: tempo_confidence, dtype: float64
        Confidence indication for the tempo

    Name: tempo_track, dtype: float64
        Tempo for the entire track [bpm]

    Name: key, dtype: int
        Musical key for the section [0 = C, 1 = C#, 2 = D, etc]

    Name: key_confidence, dtype: float64
        Confidence indicator for the key per section

    Name: key_track, dtype: int
        Musical key for the track [0 = C, 1 = C#, 2 = D, etc]

    Name: mode, dtype: int
        Musical modality, or scale, for the section [0 = Minor, 1 = Major]

    Name: mode_confidence, dtype: float64
        Confidence indicator for the mode per section

    Name: time_signature, dtype: int
        The time signtature of the section given in beats per measure

    Name: time_signature_confidence, dtype: float64
        Confidence indicator for the time signature

    Name: time_signature_track, dtype: int
        The time signtature of the track given in beats per measure

    Name: danceability, dtype: float64
        Value indicating the amount of danceability of the track, between 0.0 - 1.0

    Name: speechiness, dtype: float64
        Value indicating the confidence of being a speech work instead of music of the track, between 0.0 - 1.0

    Name: acousticness, dtype: float64
        Value indicating the amount of acousticness of the track, between 0.0 - 1.0

    Name: instrumentalness, dtype: float64
        Value indicating the confidence of being an instrumental track of the track, between 0.0 - 1.0

    Name: liveness, dtype: float64
        Value indicating the confidence of being a live performance of the track, between 0.0 - 1.0

    Name: energy, dtype: float64
        Value indicating the amount of emotional energy of the track, between 0.0 - 1.0

    Name: valence, dtype: float64
        Value indicating the amount of musical positivity of the track, between 0.0 - 1.0

    Name: loudness, dtype: float64
        Average loudness of the section [dB]

    Name: loudness_track, dtype: float64
        Average loudness of the track [dB]
