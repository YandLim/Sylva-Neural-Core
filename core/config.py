"""All the needed variabels from accross the program"""

from dotenv import load_dotenv
import os

load_dotenv()

NLU_MODEL_PATH = os.getenv("RASA_MODEL_PATH")
TTS_MODEL_NAME = os.getenv("TTS_MODEL_NAME")
TTS_MODEL_PATH = os.getenv("TTS_MODEL")
STT_MODEL = os.getenv("STT_MODEL")
SERPAPI_APIKEY = os.getenv("SERPAPI_APIKEY")

LOG_FOLDER = "logs/"