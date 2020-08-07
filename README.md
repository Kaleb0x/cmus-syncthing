# cmus-syncthing
Exports cmus playlists to a specific directory (or sync directory) that can be synced with another device using Syncthing. It can be used to export cmus playlists and their corresponding tracks to an Android smartphone running Syncthing.

## Requirements
See [requirements.txt](requirements.txt).

## Installation
### Manual installation
```
python setup.py build
sudo python setup.py install
```

### Archlinux
A [package](https://aur.archlinux.org/packages/cmus-syncthing/) is available on AUR.

## Configuration
### Minimal configuration
Before running cmus-syncthing for the first time, you need to generate a configuration file. To do so, run : 
```
cmus-syncthing init
```

This command will generate a minimal configuration file located in $XDG_CONFIG_HOME containing the playlist and sync folders and a verbosity option.

### Playlist exclusion
You can also exclude specific playlists from syncing. To do so, add their exact names in the configuration file as follows :
```
[Options]
exclude=playlist1,playlist2
```

A [configuration file template](share/cmus-syncthing.conf) is available for further details.

### systemd unit files
systemd [service](share/cmus-syncthing.service) and [timer](share/cmus-syncthing.timer) unit files can be used to run cmus-syncthing. 

## Running
### Manual running
You can run cmus-syncthing manually from the command line when required :
```
$ cmus-syncthing
```

### systemd service
Each system user can start/enable the provided systemd timer on a user level to sync their playlists. The timer runs cmus-syncthing every 15 minutes. Once the files are properly installed on your system, you can enable it by running :
```
$ systemctl --user enable cmus-syncthing.timer
```

## Contribution
Contributions are welcome. Please read the [contribution guidelines](CONTRIBUTING.md) beforehand.

## Licensing
This work is under the 0-clause BSD license. I would be very grateful to anyone who mentions me in any derivative work and distributes it back to the community. I'd rather see people act wisely as a trait, not by legal requirement.
