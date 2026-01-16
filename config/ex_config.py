"""All the external variabels needed for accross the program"""

from dotenv import load_dotenv
import os

load_dotenv()

NLU_MODEL_PATH = "rasa_nlu\models\sylva_neural.tar.gz"
TTS_MODEL_NAME = "p294"
TTS_MODEL_PATH = "tts_models/en/vctk/vits"
STT_MODEL = "small.en"
SERPAPI_APIKEY = os.getenv("SERPAPI_APIKEY")
