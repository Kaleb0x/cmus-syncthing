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
## Configuration
Before running cmus-syncthing for the first time, you need to generate a configuration file. To do so, run : 
```
cmus-syncthing init
```

## Contribution
Contributions are welcome. Please read the [contribution guidelines](CONTRIBUTING.md) beforehand.

## Licensing
This work is under the 0-clause BSD license. I would be very grateful to anyone who mentions me in any derivative work and distributes it back to the community. I'd rather see people act wisely as a trait, not by legal requirement.
