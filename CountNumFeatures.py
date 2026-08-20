import spotipy
from spotipy.oauth2 import SpotifyOAuth
import streamlit as st
import pandas as pd
import os
import requests
import json

"""
Check to see how many requests to Recco Beats are returning with data

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