import time
from tqdm import tqdm

# Simple loop wrapper
for i in tqdm(range(100), desc="Processing items"):
    time.sleep(0.05)  # Simulate work