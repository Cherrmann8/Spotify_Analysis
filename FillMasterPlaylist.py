import spotipy
from spotipy.oauth2 import SpotifyOAuth
import streamlit as st
import pandas as pd
import os
import requests
import json

"""
Create and fill a master playlist containing all songs across all playlists and library

"""


# === GOBAL VARIABLES & AUTHENTICATION ===


CLIENT_ID = os.environ.get('CLIENT_ID') # Spotify client id (thats me!)
CLIENT_SECRET = os.environ.get('CLIENT_SECRET') # Spotify secret id (thats my secret code so people can't access my account)
REDIRECT_URI = 'http://127.0.0.1:5000'


# Connect to Spotify API via authentication

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope='playlist-read-private playlist-modify-private user-library-modify'
    )
)


# === Create the master playlist ===


# WARNING - THIS IS DONE! CONSIDER REMOVING
# new_playlist = sp.current_user_playlist_create("The Mixin Pot", False, False, "every song ever")
# print(json.dumps(new_playlist, indent=4))


# === Create a list of a tracks across all playlists and library ===


print('Gathering all songs...\n')

# Get all playlists

all_playlists = []
sp_playlist_offset = 0

while True:
    # print(f'loop - offset: {sp_playlist_offset}')
    sp_all_playlists = sp.current_user_playlists(limit=50, offset=sp_playlist_offset)
    sp_playlists_found = len(sp_all_playlists['items'])
    # print(sp_playlists_found)
    sp_playlist_offset += sp_playlists_found

    for playlist in sp_all_playlists['items']:
        if playlist['owner']['id'] == 'motley_':
            all_playlists.append((playlist['name'], playlist['id']))

    if sp_playlists_found < 50:
        break

print(f'Found {len(all_playlists)} playlists...\n')

# Create a dictionary of all tracks from across all playlists

all_tracks = {}
duplicate_tracks = 0

for playlist_id in all_playlists:
    sp_track_offset = 0

    while True:
        sp_playlist_tracks = sp.playlist_items(playlist_id[1], fields='items(item(id, name))', limit=50, offset=sp_track_offset)
        sp_tracks_found = len(sp_playlist_tracks['items'])
        sp_track_offset += sp_tracks_found

        for item in sp_playlist_tracks['items']:
            if item['item']['id'] in all_tracks:
                duplicate_tracks += 1
            else:
                all_tracks[item['item']['id']] = item['item']['name']

        if sp_tracks_found < 50:
            print(f'Found {sp_track_offset} tracks in playlist: {playlist_id[0]}...')
            break

print(f'Found {duplicate_tracks} duplicate tracks across playlists...\n')

# Add all tracks from library to dictionary

sp_library_tracks = sp.current_user_saved_tracks(3)
sp_track_offset = 0
duplicate_tracks = 0

while True:
    sp_library_tracks = sp.current_user_saved_tracks(limit=50, offset=sp_track_offset)
    sp_tracks_found = len(sp_library_tracks['items'])
    sp_track_offset += sp_tracks_found

    for item in sp_library_tracks['items']:
        if item['track']['id'] in all_tracks:
            duplicate_tracks += 1
        else:
            all_tracks[item['track']['id']] = item['track']['name']

    if sp_tracks_found < 50:
        print(f'Found {sp_track_offset} tracks in library...')
        break

print(f'Found {duplicate_tracks} duplicate tracks in library...\n')


print(f'Found {len(all_tracks)} tracks...\n')

# === Add all tracks on list to master playlist ===

print(f'Adding tracks to master playlist...\n')

