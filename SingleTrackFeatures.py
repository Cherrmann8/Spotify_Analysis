import spotipy
from spotipy.oauth2 import SpotifyOAuth
import streamlit as st
import pandas as pd
import os
import requests
import json

"""
Get the Audio Features from Recco Beats of a single track using the tracks Spotify ID

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


trackID = '5ISRNtWOdRbCsDGBzl8pxA'


print(f'Sending request...')

# Get audio features
url = 'https://api.reccobeats.com/v1/audio-features'
qparams = {'ids': [trackID]}
payload = {}
headers = {'Accept': 'application/json'}
response = requests.request("GET", url, headers=headers, data=payload, params=qparams)

jsonResponse = json.loads(response.text)
print(jsonResponse)


print('Done!')