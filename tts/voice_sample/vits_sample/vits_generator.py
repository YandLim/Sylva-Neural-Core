"""This file made so Every voice in vits can be tested efficiently"""

# Importing
from TTS.api import TTS
import os

status = {
    "success": [],
    "failed": []
}

# Load model
model_name = "tts_models/en/vctk/vits"
tts = TTS(model_name)

output_dir = "vits_sample"
os.makedirs(output_dir, exist_ok=True)

# Looping throught every voice models in vits
with open("vits_models.txt") as f:
    names = [line.strip() for line in f]

for name in names:
    print(f"\nMaking voice sample of {name}\n")
    file_path = os.path.join(output_dir, f"{name} Sample.wav")

    try:
        tts.tts_to_file(
            text="Sylva Is online",
            speaker=name,
            file_path=file_path
        )

        status["success"].append(name)
        print(f"\n{name} Sample is Success\n")
    except Exception as e:
        print(f"\nFailed: {e}")
        status["failed"].append(name)
        print(f"{name} Sample is failed\n")

print(f"All set done\nSuccess: {len(status['success'])}\nFailed: {len(status['failed'])}({status['failed']})")

