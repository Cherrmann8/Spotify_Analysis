import json
from pathlib import Path
from tqdm import tqdm

"""
Go through the entire cleanedLibrary.json file and create a new json file that includes the "First Listen Dates" variable
"""


# GOBAL VARIABLES

STREAMING_HISTORY_PATH = 'C:/Users/charl/Documents/VSC Python Projects/Spotify_Analysis/Spotify Data/Extended Streaming History'
CACHED_LIBRARY_PATH = '2026-10-10_Library.json'

print('Updating all songs with first listen dates...\n')


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

print('Building translation dict...')

translation_dict = {}

for id in library:
    translation_dict[library[id]['name']] = id

print('Built...')


# === Loop through all files in the extended listening folder and see if they contain Track Ids in our cached library ===

print('Looping through listening history files...')

total_plays = 0
finds = 0

folder_path = Path(STREAMING_HISTORY_PATH)
file_paths = list(folder_path.glob("*.json"))

print(f"Found {len(file_paths)} files...")

# for i in tqdm(range(len(file_paths)), desc="Processing files"): #                   <--- This shit is so cool
# file_path = file_paths[i]
file_path = file_paths[0]
# print(f"Reading File: {file_path.name}...")

with open(file_path, "r", encoding="utf-8") as file:
    try:
        data = json.load(file)
        
        for item in data:
            
            if item['spotify_track_uri'] != None: #                                                                   Check for matching Spotify IDs
                track_id = item['spotify_track_uri'][-22:]
                
                if track_id in library:
                    if library[track_id]['first listen'] == '':
                        library[track_id]['first listen'] = item['ts']
                        finds += 1
                
            if item['master_metadata_track_name'] != None and item['master_metadata_album_artist_name'] != None: #    Check for matching names
                name = f'{item['master_metadata_track_name']} - {item['master_metadata_album_artist_name']}'

                print('here 1')

                if name in translation_dict:
                    print('here 2')
                    if library[translation_dict[name]]['first listen'] == '':
                        print('here 3')
                        library[translation_dict[name]]['first listen'] = item['ts']
                        finds += 1

            total_plays += 1
            
    except json.JSONDecodeError:
        print(f"Error: {file_path.name} is not a valid JSON file.")
    except TypeError:
        print(item)


print(f'\nTotal plays: {total_plays}')
print(f'Finds: {finds}\n')


# === Save the updated library ===

print('Saving file...')

file_path = CACHED_LIBRARY_PATH
try:
    with open(file_path, "w") as f:
        # Use 'indent=4' for human-readable formatting (pretty printing)
        json.dump(library, f, indent=4)
    print(f"Data successfully saved to {file_path}\n")
except IOError as e:
    print(f"Error saving file: {e}\n")

print('Done!')