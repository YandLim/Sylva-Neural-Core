# Importing modules
import speech_recognition as sr
from utils import logger
from core import config
import whisper
import audioop

# Define class and variabels
log = logger.get_logger(__name__)
model = config.STT_MODEL
stt_model = whisper.load_model(model)
recognizer = sr.Recognizer()

# List of error text
error_text = [".", "You", "Okay.", "Thank you."]

# Speech to text functionality
def speech_recognition() -> str:
    while True:
        try:
            # Activate microphone access
            with sr.Microphone() as source:
                audio = recognizer.listen(source, timeout=1, phrase_time_limit=10) # Listening
                rms = audioop.rms(audio.frame_data, 2) # Audio level
                log.debug(f"User rms: {rms}") # Print audio level

                # If audio shorter than 0.16 second or audio level is smaller than 85, count as invalid 
                if len(audio.frame_data) < 6000 or rms < 85:
                    return None
            
            # Convert user audio into wav file
            user_wav = audio.get_wav_data()
            log.info("Processing voice")
            with open("user_wav.wav", "wb") as f:
                f.write(user_wav)

            # Whisper STT
            result = stt_model.transcribe(
                "user_wav.wav",
                language="en",
                task="transcribe",
                no_speech_threshold=0.95,
                fp16=False,
                temperature=0.2
            )

            if result.get("no_speech_prob", 0) > 0.90:
                return None

            # Return the extracted text
            text = result["text"].strip()
            if text:
                # Checking if there is invalid word in the result
                if len(text.split()) == 1 and any(text == error for error in error_text):
                    return None
                log.debug(f"stt proccess return {text}")
                return(text)
            else:
                return None

        # Return None if timeout occured
        except sr.WaitTimeoutError:
            return None
        
        # Sending error message if something went wrong
        except Exception as e:
            log.error(f"Something went wrong: {e}")
            return None
