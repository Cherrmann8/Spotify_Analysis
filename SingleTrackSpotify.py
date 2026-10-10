import spotipy
from spotipy.oauth2 import SpotifyOAuth
import streamlit as st
import pandas as pd
import os
import requests
import json
from datetime import date


"""
FOR TESTING

Get a single track from user playlist & library

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
        scope='playlist-read-private'
    )
)

sp_playlist = sp.current_user_playlists(limit=3)

print(json.dumps(sp_playlist, indent=4))
print("\n\n")

sp_playlist_track = sp.playlist_items(sp_playlist['items'][2]['id'], limit=1)

print(json.dumps(sp_playlist_track, indent=4))
print("\n\n")

item = sp_playlist_track
test_track = {}

test_track['name'] = f'{item['item']['name']} - {item['item']['artists'][0]['name']}'
test_track['title'] = item['item']['name']
test_track['arist'] = item['item']['artists'][0]['name']
test_track['album'] = item['item']['album']['name']
test_track['track #'] = item['item']['track_number']
test_track['uri'] = item['item']['uri']
test_track['playlists'] = []
test_track['first listen'] = ''
test_track['features'] = {}

print(json.dumps(test_track, indent=4))
print("\n\n")

sp_library_track = sp.current_user_saved_tracks(limit=1)

print(json.dumps(sp_library_track, indent=4))