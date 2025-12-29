# script2.py
"""
Play randomly selected audio files with category-specific behavior
"""

import time
import random
import numpy as np
from pathlib import Path
from pygame import mixer

# Initialize pygame mixer for audio playback
mixer.init()

AUDIO_DIR = Path("audio_files")


def load_audio_files():
    """Load and categorize all audio files"""
    cat1_files = list(AUDIO_DIR.glob("cat1_*.wav"))
    cat2_files = list(AUDIO_DIR.glob("cat2_*.wav"))
    cat3_files = list(AUDIO_DIR.glob("cat3_*.wav"))
    threat_file = AUDIO_DIR / "threat.wav"

    print(f"Loaded {len(cat1_files)} cat1 files")
    print(f"Loaded {len(cat2_files)} cat2 files")
    print(f"Loaded {len(cat3_files)} cat3 files")
    print(f"Threat file: {threat_file.exists()}")

    return cat1_files, cat2_files, cat3_files, threat_file


def play_audio(file_path):
    """Play an audio file and wait for it to finish"""
    print(f"Playing: {file_path.name}")
    mixer.music.load(str(file_path))
    mixer.music.play()

    # Wait for the audio to finish
    while mixer.music.get_busy():
        time.sleep(0.1)


def wait_normal(mean, std, min_val=None):
    """Wait for a duration sampled from normal distribution"""
    wait_time = np.random.normal(mean, std)
    if min_val is not None:
        wait_time = max(wait_time, min_val)
    print(f"Waiting {wait_time:.2f} seconds...")
    time.sleep(wait_time)


def main():
    cat1_files, cat2_files, cat3_files, threat_file = load_audio_files()

    # Combine all files for random selection
    all_files = cat1_files + cat2_files + cat3_files

    if not all_files:
        print("ERROR: No audio files found!")
        return

    print("\nStarting playback loop...\n")

    while True:
        # Wait before playing next sound: X ~ N(10, 3^2) = N(10, 9)
        wait_normal(mean=10, std=3)

        # Randomly select a file
        selected_file = random.choice(all_files)

        # Play the selected file
        play_audio(selected_file)

        # Determine category and apply logic
        if selected_file in cat1_files:
            print("Category 1 file detected")

            # Wait X ~ N(2, 1) where X >= 0
            wait_normal(mean=2, std=1, min_val=0)

            # 75% chance to play threat
            if random.random() < 0.75:
                print("Playing threat (75% chance triggered)")
                play_audio(threat_file)
            else:
                print("Skipping threat (25% chance triggered)")

            # Wait 2 seconds after threat logic
            print("Waiting 2 seconds...")
            time.sleep(2)

        elif selected_file in cat2_files:
            print("Category 2 file detected")
            # Wait additional 2 seconds
            print("Waiting additional 2 seconds...")
            time.sleep(2)

        else:
            print("Category 3 file detected (no special behavior)")

        print("-" * 50)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nPlayback stopped by user")
        mixer.quit()
