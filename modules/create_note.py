from utils import logger, play_voice
import random

log = logger.get_logger(__name__)

note_create_confirm= [
    "Noted, Master. Your message has been saved.",
    "Acknowledged. The note has been created successfully.",
    "Done. I have stored the note for you, Sir.",
    "Your note is recorded and safely stored.",
    "Confirmed. The note has been added to your records.",
    "Understood, Master. I have saved that as a note.",
    "Note creation complete. Information secured.",
    "Saved. You may continue, Sir.",
    "The note has been logged successfully.",
    "Completed. Your note is now stored."
]


def create_note(tts_agent, value):
    try:
        if len(value) > 7:
            with open ("user_note/user_note.txt", "w", encoding="utf-8") as f:
                log.debug("Writing down...")
                f.write(value)
        
            confirmation_phrase = random.choice(note_create_confirm)
            phrase_path = tts_agent.sylva_voice(confirmation_phrase, "note_created.wav")
            play_voice.play_sound(phrase_path)
            return
        
        log.info("Invalid note")
        return

    except Exception as e:
        log.error(f"Something went wrong: {e}")
        return