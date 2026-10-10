import spotipy
from spotipy.oauth2 import SpotifyOAuth
import streamlit as st
import pandas as pd
import os
import requests
import json
from datetime import date


"""
Create and fill a json file containing all songs across all playlists and library

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
        scope='playlist-read-private playlist-modify-private user-library-modify user-library-read'
    )
)


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
        sp_playlist_tracks = sp.playlist_items(playlist_id[1], limit=50, offset=sp_track_offset)
        sp_tracks_found = len(sp_playlist_tracks['items'])
        sp_track_offset += sp_tracks_found

        for item in sp_playlist_tracks['items']:
            track_id = item['item']['id']

            if track_id in all_tracks:
                duplicate_tracks += 1
                all_tracks[track_id]['playlists'].append(playlist_id[0])
            else:
                all_tracks[track_id] = {}
                all_tracks[track_id]['name'] = f'{item['item']['name']} - {item['item']['artists'][0]['name']}'
                all_tracks[track_id]['title'] = item['item']['name']
                all_tracks[track_id]['arist'] = item['item']['artists'][0]['name']
                all_tracks[track_id]['album'] = item['item']['album']['name']
                all_tracks[track_id]['track #'] = item['item']['track_number']
                all_tracks[track_id]['uri'] = item['item']['id']
                all_tracks[track_id]['playlists'] = []
                all_tracks[track_id]['first listen'] = ''
                all_tracks[track_id]['features'] = {}

                all_tracks[track_id]['playlists'].append(playlist_id[0])


        if sp_tracks_found < 50:
            print(f'Found {sp_track_offset} tracks in playlist: {playlist_id[0]}...')
            break

print(f'Found {duplicate_tracks} duplicate tracks across playlists...\n')

# Add all tracks from library to dictionary

# sp_library_tracks = sp.current_user_saved_tracks(3)
sp_track_offset = 0
duplicate_tracks = 0

while True:
    sp_library_tracks = sp.current_user_saved_tracks(limit=50, offset=sp_track_offset)
    sp_tracks_found = len(sp_library_tracks['items'])
    sp_track_offset += sp_tracks_found

    for item in sp_library_tracks['items']:
        track_id = item['track']['id']

        if track_id not in all_tracks:
            all_tracks[track_id] = {}
            all_tracks[track_id]['name'] = f'{item['track']['name']} - {item['track']['artists'][0]['name']}'
            all_tracks[track_id]['title'] = item['track']['name']
            all_tracks[track_id]['arist'] = item['track']['artists'][0]['name']
            all_tracks[track_id]['album'] = item['track']['album']['name']
            all_tracks[track_id]['track #'] = item['track']['track_number']
            all_tracks[track_id]['uri'] = item['track']['id']
            all_tracks[track_id]['playlists'] = []
            all_tracks[track_id]['first listen'] = ''
            all_tracks[track_id]['features'] = {}
            duplicate_tracks += 1

    if sp_tracks_found < 50:
        print(f'Found {sp_track_offset} tracks in library...')
        break

print(f'Found {duplicate_tracks} unassigned tracks in library...\n')


print(f'Found {len(all_tracks)} tracks...\n')

# === Save tracks to a json file and include todays date in the title ===

file_path = f"{date.today()}_Library.json"

print(f'Saving file "{file_path}"...')

try:
    with open(file_path, "w") as f:
        # Use 'indent=4' for human-readable formatting (pretty printing)
        json.dump(all_tracks, f, indent=4)
    print(f'Data successfully saved to "{file_path}"')
except IOError as e:
    print(f"Error saving file: {e}")

print('Done!')
