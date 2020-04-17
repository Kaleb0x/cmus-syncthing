# cmus-syncthing

Exports cmus playlists to a specific directory that can be synced with another device using Syncthing. It can be used to export cmus playlists and their corresponding tracks to an Android smartphone running Syncthing.

## Prerequisites
Requires python >= 3.5.

## Setup
The *\[Directories\]* section of cmus-syncthing.conf must be edited beforehand as follows :
```
[Directories]
playlists=/path/to/cmus/playlists
syncthing=/path/to/sync/directory
```

cmus playlists are usually stored in ~/.config/cmus/playlists.

## Manual sync
The config file must specify both playlists and syncthing directories before running cmus-syncthing. Running cmus-syncthing.py will then create two subdirectories in the syncthing directory : 
  - *playlists* that will be populated with cmus playlists as .m3u8 files
  - *tracks* where all the tracks found in the playlists will be copied

For those who want to run it periodically using systemd timers, unit configuration files are provided.

## Contribution
Contributions are welcome. Please read the [contribution guidelines](.github/CONTRIBUTING.md) beforehand.

## Licensing
This work is under the 0-clause BSD license. I would be very grateful to anyone who mentions me in any derivative work and distributes it back to the community. I'd rather see people act wisely as a trait, not by legal requirement.
