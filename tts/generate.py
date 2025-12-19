"""This code form as bridge for voice generation in linux from windows"""

# Importing modules 
from TTS.api import TTS
import json
import sys
import os

# Load model
model = sys.argv[1]
tts = TTS(model)
print("TTS model activate", flush=True)

while True:
    # Getting data
    line = sys.stdin.readline().strip()
    if not line:
        continue

    try:
        # Tdying up the data
        data = json.loads(line)
        text = data["text"]
        speaker = data["speaker"]
        language = data["language"] if data["language"] else None
        outfile = data["outfile"]

        # Excute the tts
        if language is not None:
            tts.tts_to_file(
                text=text, 
                speaker=speaker, 
                language=language, 
                file_path=outfile, 
                temperature=0.3, 
                top_k=40, 
                top_p=0.75, 
                enable_text_splitting=True, 
                speed=0.28
            )
            
        else:
            tts.tts_to_file(
                text=text, 
                speaker=speaker, 
                file_path=outfile, 
                temperature=0.8, 
                top_k=100, 
                top_p=0.9, 
                enable_text_splitting=True, 
            )
        
        print(json.dumps({"file": outfile}), flush=True)

    except Exception as e:
        print(json.dumps({"error": str(e)}), flush=True)