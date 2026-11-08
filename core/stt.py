"""Listens, transcribes, and forwards user speech without interpretation or decision logic."""

# Importing modules
import speech_recognition as sr
from utils import logger
from config import ex_config, in_config
import whisper
import audioop

# Define class and variabels
system_log = logger.get_logger(__name__, system=True)
model = ex_config.STT_MODEL
stt_model = whisper.load_model(model)
recognizer = sr.Recognizer()

user_wav_path = in_config.USER_WAV

# List of error text
SYLVA_ALIASES = [
    "silva",
    "silver",
    "sofa",
    "shilpa",
    "snail fire",
    "selva",
    "silvah",
]

error_text = [".", "You", "Okay.", "Thank you."]

# Speech to text functionality
def speech_recognition() -> str:
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        while True:
            try:
                # Activate microphone access
                audio = recognizer.listen(source, timeout=0.4, phrase_time_limit=3) # Listening
                rms = audioop.rms(audio.frame_data, 2) # Audio level
                system_log.debug(f"User rms: {rms}") # Print audio level

                # If audio shorter than 0.16 second or audio level is smaller than 85, count as invalid 
                if len(audio.frame_data) < 5000 or rms < 90:
                    return None

                # Convert user audio into wav file
                user_wav = audio.get_wav_data()
                system_log.info("Processing voice")
                with open(user_wav_path, "wb") as f:
                    system_log.info("Writing command into wav file")
                    f.write(user_wav)

                # Whisper STT
                system_log.info("Transcribing voice")
                result = stt_model.transcribe(
                    user_wav_path,
                    language="en",
                    task="transcribe",
                    fp16=False,
                    temperature=0.2
                )
                
                system_log.info("Successfully transcribing")
                if result.get("no_speech_prob", 0) > 0.90:
                    system_log.info("Returning None as command")
                    return None

                # Return the extracted text
                text = result["text"].strip()
                if text:
                    # Checking if there is invalid word in the result
                    if len(text.split()) <= 1 and any(error in text for error in error_text):
                        return None
                    
                    # Handle invalid error word for Sylva
                    for aliases in SYLVA_ALIASES:
                        if aliases in text:
                            text = text.replace(aliases, "sylva")

                    return(text)
                else:
                    system_log.info("Returning None as command")
                    return None

            # Return None if timeout occured
            except sr.WaitTimeoutError:
                return None
            
            # Sending error message if something went wrong
            except Exception as e:
                system_log.error(f"Something went wrong: {e}")
                return None
