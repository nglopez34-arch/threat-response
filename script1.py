# script1.py
"""
Generate TTS audio files using Coqui TTS (auto-downloads models on first run)
Install: pip install TTS
"""

import os
from pathlib import Path
from TTS.api import TTS

# Define your three categories
cat_1 = [
    "gun",
    "handgun",
    "rifle",
    "shotgun",
    "pointing a firearm",
    "knife",
    "large blade",
    "machete",
    "sword",
    "axe",
    "raised baseball bat",
    "crowbar",
    "metal pipe",
    "hammer raised overhead",
    "screwdriver aimed forward",
    "I’m going to kill you",
    "I will shoot you",
    "I have a gun",
    "reaching into waistband after threat",
    "charging toward officer",
    "vehicle accelerating toward officer",
    "attempted gun grab",
    "improvised explosive device",
    "firebomb",
    "Molotov cocktail",
    "strangulation attempt",
    "choking from behind",
    "multiple attackers rushing"
]


cat_2 = [
    "clenched fists",
    "aggressive yelling",
    "verbal threats",
    "advancing while yelling",
    "shoving",
    "pushing",
    "swinging fists",
    "attempted punch",
    "grabbing arm",
    "throwing small objects",
    "spitting",
    "hostile posturing",
    "intoxicated aggression",
    "cornering behavior",
    "shoulder-checking",
    "removing shirt to fight",
    "crowding personal space aggressively"
]


cat_3 = [
    "cell phone",
    "wallet",
    "keys",
    "water bottle",
    "backpack",
    "sunglasses",
    "book",
    "laptop",
    "I don’t understand",
    "I’m just walking home"
]


OUTPUT_DIR = Path("audio_files")
OUTPUT_DIR.mkdir(exist_ok=True)

# Initialize TTS with a multi-speaker model
# This will auto-download on first run
print("Initializing TTS model (will auto-download on first run)...")
tts = TTS(model_name="tts_models/en/vctk/vits", progress_bar=False, gpu=False)

# Get available speakers (VCTK has 109 speakers)
speakers = tts.speakers[:5]  # Use first 5 speakers as our 5 voices
print(f"Using speakers: {speakers}")


def generate_audio(text, speaker, output_file):
    """Generate audio using Coqui TTS"""
    output_path = OUTPUT_DIR / output_file
    tts.tts_to_file(
        text=text,
        speaker=speaker,
        file_path=str(output_path)
    )
    print(f"Generated: {output_path}")


def main():
    # Generate cat_1 files
    for i, text in enumerate(cat_1, 1):
        for j, speaker in enumerate(speakers, 1):
            filename = f"cat1_item{i}_voice{j}.wav"
            generate_audio(text, speaker, filename)

    # Generate cat_2 files
    for i, text in enumerate(cat_2, 1):
        for j, speaker in enumerate(speakers, 1):
            filename = f"cat2_item{i}_voice{j}.wav"
            generate_audio(text, speaker, filename)

    # Generate cat_3 files
    for i, text in enumerate(cat_3, 1):
        for j, speaker in enumerate(speakers, 1):
            filename = f"cat3_item{i}_voice{j}.wav"
            generate_audio(text, speaker, filename)

    # Generate the "threat" audio (using first speaker)
    generate_audio("threat", speakers[0], "threat.wav")

    print(f"\nAll audio files generated in '{OUTPUT_DIR}' directory!")
    print(f"Total files: {len(cat_1) * 5 + len(cat_2) * 5 + len(cat_3) * 5 + 1}")


if __name__ == "__main__":
    main()
