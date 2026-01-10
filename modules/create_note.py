"""create_note. Responsible for note creation, validation, and storage."""

# Importing modules
from utils.dataclasess import ModuleResults
from utils import logger
from datetime import datetime
from config import in_config
import random 
import os

# Define logger
system_log = logger.get_logger(__name__, system=True)
user_log = logger.get_logger(__name__, system=False)

# Confirmation templates
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

# Define the path and title template
note_dir = in_config.NOTES_DIR
current_time = datetime.now().strftime("%m-%d-%Y %H_%M_%S {title}.txt")

# Main function
def create_note(value: str) -> ModuleResults:
    try:
        # Checking the availability of the note directory
        os.makedirs(note_dir, exist_ok=True)

        # Checking for invalid note
        system_log.debug(f"Value len: {len(value)}")
        if len(value) > 7: 
            # Make note title
            words = value.split()[1:3]
            note_title = " ".join(word for word in words) if words else "note"
            complete_title = current_time.format(title=note_title)
            system_log.info(f"Creating note: {complete_title}")

            # Writing note
            note_path = os.path.join(note_dir, complete_title)
            with open (note_path, "w", encoding="utf-8") as f:
                system_log.debug(f"Note value: {value}")
                f.write(value)

            # Voice confirmation
            sentence = random.choice(note_create_confirm)
            return ModuleResults(sentence=sentence, context="create_note_module")

        # raise IndexError if note is invalid
        system_log.warning("Invalid note")
        raise IndexError("The word in note is less than 7 and count as not valid")

    # Error occured
    except Exception as e:
        system_log.error(f"Something went wrong: {e}")
        raise

if __name__ == "__main__":
    create_note(None)
