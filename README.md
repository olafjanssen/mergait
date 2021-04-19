# MERGait
This package assists in reading and processing running gait related data, varying from raw (iPhone) activity and IMU data to footpod per-step data.

## Overview
This package is developed as part of the Music Enabled Running project which explores the relationship between the (subconscious) perception of music
and the way we run to that music. We hypothesize that by collecting enough data about gait parameters during running and combining it with an extensive set of musical parameters that the person is listening to, we can steer a runner to a different (and ultimately better) running pattern. The analysis will be personalized because we expect our reaction to music to be highly personal as well. We take it beyond syncing your run to a certain rythm of BPM, and take into account the impact of music on your emotions and attention.

As part of this project, we developed a test platform in which data is gathered and combined from recreational runners:
* IMU, GPS, and activity data from a waist-worn iPhone
* foot placement from RunScribe footpods
* music features and analysis data from Spotify

This package can be used to analyze this, and related, data. A grasp of what is computed:
* symmetry between left and right foot parameters
* gait extraction from IMU signals
* symmetry in the IMU signals

## Installation
MERGait is compatible with python v3.6+

**You can install MERGait via pip:**
```sh
pip install mergait
```

## Basic usage
We refer to the example notebooks for how to apply the standard recipes for loading and analyzing the gait and music data.

In addition, you can find the reference documentation in MarkDown [here](https://github.com/olafjanssen/mergait/tree/main/docs/md/mergait) or as [web page](https://olafjanssen.github.io/mergait).

Read [here](https://github.com/olafjanssen/mergait/blob/main/data/README.md) how to obtain a sample data set and read the [codebook](https://github.com/olafjanssen/mergait/blob/main/data/codebook.md) of the sample data.

## Contributing to the project
Please contact us if you want to contribute to this project or you are interested in the data.

## Acknowledgements
This package was developed as part of the Music Enabled Running research project conducted at the [centre of expertise Interaction Design (IXD)](https://www.ixdfontysict.nl/), which is a research chair at Fontys School of Information and Communication Technology (FHICT), department of [Fontys](https://fontys.nl/) University of Applied Sciences, Eindhoven, The Netherlands.

This research project was additionally funded by:

* Vitality Living Lab
* Nano4Sports

Both initiatives of the [Cluster Sports & Technology](https://sportsandtechnology.com/)

## Author
Olaf T.A. Janssen

## License
MERGait is under the MIT license
