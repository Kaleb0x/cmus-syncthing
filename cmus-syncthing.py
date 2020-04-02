#!/usr/bin/env python
# -*- coding: utf-8 -*-
from cmussyncthing import SyncMachine


CONFIG_FILE = "cmus-syncthing.conf"

if __name__ == "__main__":
    sync_machine = SyncMachine(CONFIG_FILE)
    sync_machine.sync()
