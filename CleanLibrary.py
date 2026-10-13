import json
from pathlib import Path
from tqdm import tqdm
from datetime import datetime
from datetime import timezone

"""
Set first listen dates to today and remove dups
"""


# GOBAL VARIABLES

CACHED_LIBRARY_PATH = '2026-10-13_Library.json'

print('Updating all songs with first listen dates...\n')


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

print('Loaded...')


# === Loop through all files in the extended listening folder and see if they contain Track Ids in our cached library ===

print('Looping through listening history files...')

total_dups = 0
remove_ids = {}

for id in library:
    ts = datetime.now()
    ts = ts.replace(tzinfo=timezone.utc)
    library[id]['first listen'] = ts.isoformat()

    for id2 in library:
        if id2 not in remove_ids and id != id2 and library[id]['name'] == library[id2]['name']:
            library[id]['playlists'] = list(set(library[id]['playlists'] + library[id2]['playlists']))
            remove_ids[id2] = ''
            
            total_dups += 1

for id in remove_ids:
    del library[id]

print(f"Total dups removed: {total_dups}")

# === Save the updated library ===

print('Saving file...')

file_path = CACHED_LIBRARY_PATH.split('.')[0] + "_cleaned.json"
try:
    with open(file_path, "w", encoding="utf-8") as f:
        # Use 'indent=4' for human-readable formatting (pretty printing)
        json.dump(library, f, indent=4, ensure_ascii=False)
    print(f"Data successfully saved to {file_path}\n")
except IOError as e:
    print(f"Error saving file: {e}\n")

print('Done!')