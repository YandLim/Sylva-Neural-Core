"""This file made so Every voice in xtts_v2 can be tested efficiently"""

# Importing
from TTS.api import TTS
import os

status = {
    "success": [],
    "failed": []
}

# Load model
model_name = "tts_models/multilingual/multi-dataset/xtts_v2"
tts = TTS(model_name)

output_dir = "xtts_v2_sample"
os.makedirs(output_dir, exist_ok=True)

# Looping throught every voice models in xtts_v2
with open("xtts_v2_models.txt") as f:
    names = [line.strip() for line in f]

for name in names:
    print(f"\nMaking voice sample of {name}\n")
    file_path = os.path.join(output_dir, f"{name} Sample.wav")

    try:
        tts.tts_to_file(
            text="Sylva Is online",
            speaker=name,
            language="en",
            file_path=file_path
        )

        status["success"].append(name)
        print(f"\n{name} Sample is Success\n")
    except:
        status["failed"].append(name)
        print(f"\n{name} Sample is failed\n")

print(f"All set done\nSuccess: {len(status['success'])}\nFailed: {len(status['failed'])}({status["failed"]})")

