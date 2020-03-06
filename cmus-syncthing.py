#!/usr/bin/env python
import configparser
import shutil as sh
import logging
import sys
import os

CONFIG_FILE = "cmus-syncthing.conf"


def delete(dir_entry):
    if dir_entry.is_dir():
        sh.rmtree(dir_entry.path)
    else:
        os.remove(dir_entry.path)


def clean_sync_dir(plst):
    for entry in os.scandir(SYNC_DIR):
        if entry.name != "tracks" and \
           entry.name != "playlists" and \
           entry.name != ".stfolder":
            delete(entry)

    for entry in os.scandir(os.path.join(SYNC_DIR, "playlists")):
        if entry.name[:-5] not in plst or \
           entry.name[-5:] != ".m3u8":
            delete(entry)


def generate_m3u8(plst):
    full_path = os.path.join(SYNC_DIR, "playlists")

    if not os.path.isdir(full_path):
        os.mkdir(full_path)

    for playlist in plst:
        playlist_path = os.path.join(full_path, playlist + ".m3u8")

        with open(playlist_path, "w") as f:
            for track in plst[playlist]:
                track_path = os.path.basename(track) + "\n"
                track_path = os.path.join("..", "tracks", track_path)

                f.write(track_path)


def remove_deleted_tracks(plst_tracklist, drct):
    tracks_removed = False
    full_path = os.path.join(SYNC_DIR, "tracks")
    plst_track_name = {os.path.basename(x) for x in plst_tracklist}

    for track in drct:
        if track in plst_track_name:
            continue

        sync_dir_track_path = os.path.join(full_path, track)
        os.remove(sync_dir_track_path)

        logging.info("Removed track {}".format(track))
        tracks_removed = True

    return tracks_removed


def add_new_tracks(plst_tracklist, drct):
    tracks_added = False
    full_path = os.path.join(SYNC_DIR, "tracks")

    for track in plst_tracklist:
        track_name = os.path.basename(track)

        if track_name in drct:
            continue

        sync_dir_track_path = os.path.join(full_path, track_name)
        sh.copyfile(track, sync_dir_track_path)

        logging.info("Added track {}".format(track_name))
        tracks_added = True

    return tracks_added


def directory():
    drct = set()
    full_path = os.path.join(SYNC_DIR, "tracks")

    if not os.path.isdir(full_path):
        os.mkdir(full_path)

    for track in os.scandir(full_path):
        track_path = os.path.join(full_path, track.name)

        if os.path.isdir(track_path):
            sh.rmtree(track_path)
            continue

        drct.add(track.name)

    return drct


def playlists():
    plst = dict()
    plst_tracklist = set()

    for playlist in os.scandir(PLAYLIST_DIR):
        full_path = os.path.join(PLAYLIST_DIR, playlist)

        if os.path.isdir(full_path):
            continue

        plst[playlist.name] = list()

        with open(full_path, "r") as f:
            for line in iter(f.readline, ""):
                track_path = line.replace("\n", "")
                plst[playlist.name].append(track_path)
                plst_tracklist.add(track_path)

    return plst, plst_tracklist


def configuration():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)

    global PLAYLIST_DIR
    global SYNC_DIR

    try:
        PLAYLIST_DIR = config["Directories"]["playlists"]
        SYNC_DIR = config["Directories"]["syncthing"]
    except Exception:
        logging.critical("Missing playlist or sync directories in config file")
        sys.exit(1)

    if not os.path.isdir(PLAYLIST_DIR) or \
       not os.path.isdir(SYNC_DIR):
        logging.warning("Playlist or sync directories do not exist.")
        sys.exit()


if __name__ == "__main__":
    if not os.path.isfile(CONFIG_FILE):
        logging.critical("Config file not found")
        sys.exit(1)

    configuration()

    plst, plst_tracklist = playlists()
    drct = directory()

    tracks_added = add_new_tracks(plst_tracklist, drct)
    tracks_removed = remove_deleted_tracks(plst_tracklist, drct)

    if tracks_added or tracks_removed:
        generate_m3u8(plst)

    clean_sync_dir(plst)
