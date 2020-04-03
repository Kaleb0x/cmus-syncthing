# -*- coding: utf-8 -*-
import configparser
import shutil as sh
import logging
import sys
import os


class SyncMachine:
    def __init__(self, config_file):
        if not os.path.isfile(config_file):
            logging.critical("Config file not found")
            sys.exit(1)

        self.configuration(config_file)

    def configuration(self, config_file):
        config = configparser.ConfigParser()
        config.read(config_file)

        try:
            self._playlist_dir = config["Directories"]["playlists"]
            self._sync_dir = config["Directories"]["syncthing"]
        except Exception:
            logging.critical("Missing playlist or sync directories in config" +
                             " file")
            sys.exit(1)

        if not os.path.isdir(self._playlist_dir) or \
           not os.path.isdir(self._sync_dir):
            logging.warning("Playlist or sync directories do not exist.")
            sys.exit()

    def _delete_filesystem_entry(self, dir_entry):
        if dir_entry.is_dir():
            sh.rmtree(dir_entry.path)
        else:
            os.remove(dir_entry.path)

    def _clean_sync_dir(self, plst):
        for entry in os.scandir(self._sync_dir):
            if entry.name != "tracks" and \
               entry.name != "playlists" and \
               entry.name != ".stfolder":
                self._delete_filesystem_entry(entry)

        playlist_path = os.path.join(self._sync_dir, "playlists")

        if not os.path.isdir(playlist_path):
            return

        for entry in os.scandir(playlist_path):
            if entry.name[:-5] not in plst or \
               entry.name[-5:] != ".m3u8":
                self._delete_filesystem_entry(entry)

    def _generate_m3u8(self, plst):
        full_path = os.path.join(self._sync_dir, "playlists")

        if not os.path.isdir(full_path):
            os.mkdir(full_path)

        for playlist in plst:
            playlist_path = os.path.join(full_path, playlist + ".m3u8")

            with open(playlist_path, "w") as f:
                for track in plst[playlist]:
                    track_path = os.path.basename(track) + "\n"
                    track_path = os.path.join("..", "tracks", track_path)

                    f.write(track_path)

    def _remove_deleted_tracks(self, plst_tracklist, drct):
        tracks_removed = False
        full_path = os.path.join(self._sync_dir, "tracks")
        plst_track_name = {os.path.basename(x) for x in plst_tracklist}

        for track in drct:
            if track in plst_track_name:
                continue

            sync_dir_track_path = os.path.join(full_path, track)
            os.remove(sync_dir_track_path)

            logging.info("Removed track {}".format(track))
            tracks_removed = True

        return tracks_removed

    def _add_new_tracks(self, plst_tracklist, drct):
        tracks_added = False
        full_path = os.path.join(self._sync_dir, "tracks")

        for track in plst_tracklist:
            track_name = os.path.basename(track)

            if track_name in drct:
                continue

            sync_dir_track_path = os.path.join(full_path, track_name)
            sh.copyfile(track, sync_dir_track_path)

            logging.info("Added track {}".format(track_name))
            tracks_added = True

        return tracks_added

    def _directory(self):
        drct = set()
        full_path = os.path.join(self._sync_dir, "tracks")

        if not os.path.isdir(full_path):
            os.mkdir(full_path)

        for track in os.scandir(full_path):
            track_path = os.path.join(full_path, track.name)

            if os.path.isdir(track_path):
                sh.rmtree(track_path)
                continue

            drct.add(track.name)

        return drct

    def _playlists(self):
        plst = dict()
        plst_tracklist = set()

        for playlist in os.scandir(self._playlist_dir):
            full_path = os.path.join(self._playlist_dir, playlist)

            if os.path.isdir(full_path):
                continue

            plst[playlist.name] = list()

            with open(full_path, "r") as f:
                for line in iter(f.readline, ""):
                    track_path = line.replace("\n", "")
                    plst[playlist.name].append(track_path)
                    plst_tracklist.add(track_path)

        return plst, plst_tracklist

    def sync(self):
        plst, plst_tracklist = self._playlists()
        drct = self._directory()

        tracks_added = self._add_new_tracks(plst_tracklist, drct)
        tracks_removed = self._remove_deleted_tracks(plst_tracklist, drct)

        if tracks_added or tracks_removed:
            self._generate_m3u8(plst)

        self._clean_sync_dir(plst)
