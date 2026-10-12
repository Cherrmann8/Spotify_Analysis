import json


"""
Get statistics for a cached library

"""


# GOBAL VARIABLES

CACHED_LIBRARY_PATH = '2026-10-10_Library.json'


# === Load cached library ===

print('Loading cached library...')

library = None

try:
    with open(CACHED_LIBRARY_PATH, 'r', encoding='utf-8') as file:
        library = json.load(file)
except FileNotFoundError:
    print(f"Error: The file {CACHED_LIBRARY_PATH} was not found.")
except json.JSONDecodeError:
    print("Error: The file does not contain valid JSON.")

print('Loaded...\n')


# === Loop through library and gather key indicators ===

total_tracks = 0
total_assigned_playlists = 0
total_first_listen = 0
total_features = 0
total_dups = 0

for id in library:
    track = library[id]
    total_tracks += 1
    total_assigned_playlists += len(track['playlists'])
    if len(track['first listen']) > 0:
        total_first_listen += 1
    if len(track['features']) > 0:
        total_features += 1

    for id2 in library:
        if id != id2 and library[id]['name'] == library[id2]['name']:
            total_dups += 1


print(f'Total tracks: {total_tracks}\n')

print(f'Playlist assigns: {total_assigned_playlists}')
print(f'Average playlist assigns: {total_assigned_playlists/total_tracks}\n')

print(f'Total first listens: {total_first_listen}')
print(f'Missing first listens: {total_tracks - total_first_listen}\n')

print(f'Total features: {total_features}')
print(f'Missing features: {total_tracks - total_features}\n')

print(f'Total dups: {total_dups}')
