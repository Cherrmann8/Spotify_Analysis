import spotipy
from spotipy.oauth2 import SpotifyOAuth
import streamlit as st
import pandas as pd
import os
import requests
import json

"""
Basic analysis of spotify library

Field               Type	Description
-----------------------------------------------------------------------------------------------------------------------------
acousticness	    Float	Confidence (0.0 to 1.0) that the track is acoustic. Higher values indicate more natural sounds.
danceability	    Float	Suitability for dancing (0.0 to 1.0). Higher values indicate more rhythmically engaging tracks.
energy	            Float	Intensity and liveliness (0.0 to 1.0). Higher values indicate more energetic tracks.
instrumentalness	Float	Likelihood of no vocals (0.0 to 1.0). Values above 0.5 suggest instrumental tracks.
liveness	        Float	Probability of a live audience (0.0 to 1.0). Values above 0.8 strongly suggest a live track.
loudness	        Float	Average loudness in decibels (dB). Typically ranges between -60 and 0 dB.
speechiness	        Float	Presence of spoken words (0.0 to 1.0). Values above 0.66 indicate mostly speech.
tempo	            Float	Estimated tempo in beats per minute (BPM). Typically ranges between 0 and 250.
valence	            Float	Emotional tone (0.0 to 1.0). Higher values indicate a happier mood, lower values a sadder one.
"""


# GOBAL VARIABLES
# CLIENT_ID = os.environ.get('CLIENT_ID') # Spotify client id (thats me!)
# CLIENT_SECRET = os.environ.get('CLIENT_SECRET') # Spotify secret id (thats my secret code so people can't access my account)
# REDIRECT_URI = 'http://127.0.0.1:5000'


# Connect to Spotify API via authentication
# TODO - scope needs to be changed to access playlists (if I eventually do want to dynamically change playlists)
# sp = spotipy.Spotify(
#     auth_manager=SpotifyOAuth(
#         client_id=CLIENT_ID,
#         client_secret=CLIENT_SECRET,
#         redirect_uri=REDIRECT_URI,
#         scope='user-top-read'
#     )
# )

# Web browser display setup
# st.set_page_config(page_title='song analysis', page_icon=':musical_note:')
# st.title('Analysis for top songs, nerd')
# st.write('Discover insights ya nerd')

# TODO - load downloaded and cleaned Spotify data from json file for track ids
library = None
try:
    with open('./cleanedLibrary.json', 'r', encoding='utf-8') as file:
        library = json.load(file)
except FileNotFoundError:
    print("Error: The file 'newLibrary.json' was not found.")
except json.JSONDecodeError:
    print("Error: The file does not contain valid JSON.")

# create new dictionary as a more useful data structure
newLibrary = {}
for track in library:
    newLibrary[track['uri'][-22:]] = track

# TODO - I have all ids from downloading my spotify data so no need to request ids here
# # Grab some track ids from spotify api
# top_tracks = sp.current_user_top_tracks(limit=10, time_range='short_term')
# # print(json.dumps(top_tracks, indent=4))
# track_ids = [track['id'] for track in top_tracks['items']]
# track_names = [track['name'] for track in top_tracks['items']]

# TODO - Maybe remvove this at end of project because I thought I needed to convert Spotify ids to Recco ids but I do not!
# # Get Recco song ids
# url = f'https://api.reccobeats.com/v1/track?ids={', '.join(track_ids)}'
# payload = {}
# headers = {'Accept': 'application/json'}
# response = requests.request("GET", url, headers=headers, data=payload)
#
# r_dict = json.loads(response.text)
# recco_ids = [track['id'] for track in r_dict['content']]
#
# print(json.dumps(recco_ids, indent=4))

print(f'Sending {len(newLibrary)} requests...')
processedRequests = 0

# Get audio features in batches of 40 (the most recco beats can handle in one request)
uris = list(newLibrary.keys())
for i in range(0, len(library), 40):
    chunk = uris[i : i + 40]
    print(f'sending {len(chunk)}...')
    url = 'https://api.reccobeats.com/v1/audio-features'
    qparams = {'ids': chunk}
    payload = {}
    headers = {'Accept': 'application/json'}
    response = requests.request("GET", url, headers=headers, data=payload, params=qparams)

    # TODO - save audio features to a json file
    jsonResponse = json.loads(response.text)

    for trackFeatures in jsonResponse['content']:
        newLibrary[trackFeatures['href'][-22:]]['features'] = {'acousticness': trackFeatures['acousticness'], 'danceability': trackFeatures['danceability'], 'energy': trackFeatures['energy'], 'instrumentalness': trackFeatures['instrumentalness'], 'liveness': trackFeatures['liveness'], 'loudness': trackFeatures['loudness'], 'speechiness': trackFeatures['speechiness'], 'tempo': trackFeatures['tempo'], 'valence': trackFeatures['valence']}

    print(f"found {len(jsonResponse['content'])} / {len(chunk)}")
    processedRequests += len(jsonResponse['content'])

print(f'Processed {processedRequests} requests...')

print('Saving file...')

file_path = "featureLibrary.json"
try:
    with open(file_path, "w") as f:
        # Use 'indent=4' for human-readable formatting (pretty printing)
        json.dump(newLibrary, f, indent=4)
    print(f"Data successfully saved to {file_path}")
except IOError as e:
    print(f"Error saving file: {e}")

print('Done!')