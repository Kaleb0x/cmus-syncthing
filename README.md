# cmus-syncthing

Exports cmus playlists to a specific directory that can be synced with another device using Syncthing. It can be used to export cmus playlists to an Android smartphone running Syncthing.

## Prerequisites
Requires python >= 3.5.

## Setup
cmus-syncthing.conf must be edited beforehand. It contains a single section with two values as follows :
```
[Directories]
playlists=/path/to/cmus/playlists
syncthing=/path/to/sync/directory
```

cmus playlists are usually stored in ~/.config/cmus/playlists.

## Manual sync
The config file must specify both playlists and syncthing directories before running cmus-syncthing. Running cmus-syncthing.py will then populate the Syncthing directory with cmus playlists and copy the corresponding tracks.

For those who want to run it periodically using systemd timers, unit configuration files are provided.

## Known issues
- If two or more tracks have the same filename, the last track to be copied by cmus-syncthing will overwrite the others in the tracks directory. The resulting issue is that all the items in the playlists refering to these tracks will point to that last track.

## TODO
- Make a Python package out of the script

## Licensing
This work is under the 0-clause BSD license. I would be very grateful to anyone who mentions me in any derivative work and distributes it back to the community. I'd rather see people act wisely as a trait, not by legal requirement.
