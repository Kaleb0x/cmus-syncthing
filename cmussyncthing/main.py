# -*- coding: utf-8 -*-
from cmussyncthing.cmus_syncthing import SyncMachine
from xdg.BaseDirectory import xdg_config_home
from os.path import join
import sys


def main():
    config_file = join(xdg_config_home,
                       "cmus-syncthing",
                       "cmus-syncthing.conf"
                       )

    if len(sys.argv) == 2 and sys.argv[1] == "init":
        init = True
    else:
        init = False

    sync_machine = SyncMachine(config_file, init)
    sync_machine.sync()
