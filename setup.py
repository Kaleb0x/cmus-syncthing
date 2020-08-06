#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

if __name__ == "__main__":
    setup(
        name="cmus-syncthing",
        version="0.7.0",
        packages=find_packages(),
        install_requires=open("requirements.txt").read().splitlines(),
        entry_points={
            "console_scripts" : [
                "cmus-syncthing = cmussyncthing.main:main"
                ]
            }
    )
