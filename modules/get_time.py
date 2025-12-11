"""Give Sylva access into the current date"""

# Importing modules
from utils import logger, play_voice
from datetime import datetime
import random

# Define class
log = logger.get_logger(__name__)

# Sylva phrases tamplates
time_templates = [
    "The current time is {time}, Sir.",
    "It is now {time}, Master.",
    "According to my system clock, it's {time}.",
    "Time check complete. It's {time}.",
    "My readings show {time}, Sir.",
    "It is precisely {time}, Master.",
    "Clock synchronized. Current time: {time}.",
    "The time right now is {time}.",
    "System reports {time}, Sir.",
    "It’s {time}. Shall we proceed?",
    "Master, the time is {time}.",
    "As of this moment, it is {time}.",
    "I’m reporting the time as {time}.",
    "Sir, it's currently {time}.",
    "Time data retrieved. {time}.",
    "Master, the clock indicates {time}.",
    "Local time detected: {time}.",
    "It stands at {time}, Sir.",
    "My system confirms the time is {time}.",
    "The hour is {time}, Master."
]

# Get time
def current_time(tts_agent):
    cur_time = datetime.now().strftime("%H:%M:%S")
    choosen_template = random.choice(time_templates)
    sentences = choosen_template.format(time=cur_time) 
    
    # Execute text-to-speech
    voice_path = tts_agent.sylva_voice(sentences, "get_time.wav")
    play_voice.play_sound(voice_path)
