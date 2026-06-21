"""
Provides utilities for converting text into speech audio.
This module exposes a simple interface around the underlying
TTS engine, allowing control over speech rate, pitch, and
voice selection. Suitable for applications that generate
spoken messages or automated narration.
"""

# Importing libraries
from utils import logger
from config import ex_config
from typing import Any
import subprocess
import json
import os

# Define class
log = logger.get_logger(__name__)

# Get current path
current_path = os.getcwd().replace("\\", "/").replace(":", "").replace("Z", "z")
linux_tts_path = f"/mnt/{current_path}/tts"

# Make text-to-speech class
class SylvaTTSGenerator():
    # Generator setup
    def __init__(self):
        # Getting data from config.py
        self.tts_model = ex_config.TTS_MODEL_PATH
        self.tts_model_name = ex_config.TTS_MODEL_NAME

        # Define path
        self.linux_venv = f"{linux_tts_path}/tts_venv/bin/activate"
        self.generator_path = f"{linux_tts_path}/generate.py"   

        # Execute subprocess in linux
        log.debug("Running linux server")
        wsl_prompt = f"source {self.linux_venv} && python3 {self.generator_path} {self.tts_model}"
        self.worker = subprocess.Popen(
            ["wsl", "bash", "-ic", wsl_prompt],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            errors='replace',
            encoding='utf-8',
            text=True
        )

        # Make sure the worker are ready
        while True:
            if self.worker.poll() is not None:
                err = self.worker.stderr.read()
                raise RuntimeError(f"TTS worker crashed on startup: {err}")
            
            ready = self.worker.stdout.readline().strip()
            if ready == "":
                continue
            
            log.debug(f"Worker: {ready}")
            break


    # Generate the voice
    def sylva_voice(self, text:Any, outfile:str, language:str|None=None) -> str:
        mct_output_path = f"{linux_tts_path}/Output/{outfile}"
        windows_output_path = f"tts\Output"

        os.makedirs(windows_output_path, exist_ok=True)

        # Sending data to generate.py in linux
        payload = {"text":text, "speaker":self.tts_model_name, "language":language, "outfile":mct_output_path} 
        self.worker.stdin.write(json.dumps(payload) + "\n")
        self.worker.stdin.flush()

        # Double checking data received from linux server
        while True:
            response_line = self.worker.stdout.readline().strip()

            # Checking if data is json
            if not response_line.startswith("{"):
                print("LOG:", response_line)   # Optional debugging
                continue
            break
       
        # Return the generate .wav file path
        return f"{windows_output_path}\{outfile}"
    
if __name__ == "__main__":
    SylvaTTSGenerator()