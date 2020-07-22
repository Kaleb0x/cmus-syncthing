# -*- coding: utf-8 -*-
from cmussyncthing.cmus_syncthing import SyncMachine
from xdg.BaseDirectory import xdg_config_home
from os.path import join


def main():
    config_file = join(xdg_config_home,
                       "cmus-syncthing",
                       "cmus-syncthing.conf"
                       )
    sync_machine = SyncMachine(config_file)
    sync_machine.sync()
