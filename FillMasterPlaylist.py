import spotipy
from spotipy.oauth2 import SpotifyOAuth
import streamlit as st
import pandas as pd
import os
import requests
import json
from tqdm import tqdm


"""
Create and fill a master playlist containing all songs across all playlists and library

"""


# === GOBAL VARIABLES & AUTHENTICATION ===

CACHED_LIBRARY_PATH = '2026-10-13_Library_cleaned_dated.json'
MASTER_PLAYLIST_ID = '3tjHWyNUPxRceFo9lrGtzS'
CHUNK_SIZE = 100

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


# === Load cached library and build translation dictionary ===

print('Loading cached library...')

library = None

try:
    with open(CACHED_LIBRARY_PATH, 'r', encoding='utf-8') as file:
        library = json.load(file)
except FileNotFoundError:
    print(f"Error: The file {CACHED_LIBRARY_PATH} was not found.")
except json.JSONDecodeError:
    print("Error: The file does not contain valid JSON.")

print('Loaded...')

print('Building translation list...')

translation_list = []

for id in library:
    translation_list.append((id, library[id]['first listen'], library[id]['name']))

translation_list = sorted(translation_list, key=lambda x: (x[1]))

# for i in range(len(translation_list)-100, len(translation_list)):
#     print(translation_list[i])

print('Built...')

print(f'Found {len(library)} tracks...\n')

# === Add all tracks on list to master playlist ===

print(f'Adding tracks to master playlist...')

for i in tqdm(range(0, len(translation_list), CHUNK_SIZE), desc="Processing files"):
    chunk = [tup[0] for tup in translation_list[i:i + CHUNK_SIZE]]
    try:
        sp.playlist_add_items(MASTER_PLAYLIST_ID, chunk)
        # print(f"Successfully added tracks {i} to {i + len(chunk)}")
    except Exception as e:
        print(f"Error adding chunk starting at index {i}: {e}")

print('Done!')