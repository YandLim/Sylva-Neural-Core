"""Responsible for the making and executing the remind_me function without a fail"""

# Importing libraries and modules
from datetime import datetime, timedelta
from utils import logger, play_voice
from config import in_config
from typing import Literal
from pathlib import Path
import random
import time
import json
import os

# Define logger
system_log = logger.get_logger(__name__, system=True)
user_log = logger.get_logger(__name__, system=False)

# Setup the path and json file
path = Path(in_config.REMIND_ME_DIR)
os.makedirs(path, exist_ok=True)

current_month = datetime.now().strftime("%Y-%B")
reminder_path = os.path.join(path, f"{current_month}.json")
if not os.path.exists(reminder_path):
    system_log.info(f"Generate reminder json file: {reminder_path}")
    with open(reminder_path, "w", encoding="utf-8") as f:
        json.dump({"meta": {"last_id": 000}, "reminders": {}}, f, indent=2)

# Sylva's template
reminder_templates = [
    "Hey. I know you might delay this, but it’s time to '{context}'.",
    "Reminder’s up. No rush… but yeah, you should '{context}' now.",
    "You asked me to remind you. So here it is. Time to '{context}'.",
    "This is your reminder. You can ignore it… or just '{context}' now.",
    "Not trying to pressure you. Just saying, it’s time to '{context}'.",
    "Alright. Gentle reminder. You planned to '{context}' around now.",
    "I’m here to remind you. Do what you want, but it’s time to '{context}'.",
    "Reminder delivered. Even if you’re tired, '{context}' is up.",
    "Hey. This was scheduled earlier. Time to '{context}'.",
    "System check complete. Your reminder is active. '{context}'."
]

# Collecting json data 
def get_json_data() -> dict:
    with open(reminder_path, "r") as f:
        json_data = json.load(f)
    return json_data


# Adding json data
def add_json_data(json_path: Path, data: dict) -> None:
    system_log.info("Add new data to reminders.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump((data), f, indent=2)
    return


# Turn context into reminder's context and time value 
def clean_context(context: str) -> list:
    # Setup the variables 
    not_first_word = ["hi", "hey", "to"]
    not_last_word = ["in", "within", "about"]
    unused_word = ["remind", "me", "pm", "am", "second", "seconds", "minute", "minutes", "hour", "hours", "day", "days", "month"]
    cleaned_word = []

    # Remove first or last blacklist word
    def remove_edge_word(
        blacklist_words: list, 
        words: list, 
        status: Literal["first", "last"]  # Pick one first or last
    ) -> list:

        # Determine index value according to the status
        start_time = time.time()
        index = 0 if status == "first" else -1
        count = 0
        TIMEOUT = 5

        try:
            # Looping until no more blaclist word for 10 times
            while True:
                if time.time() - start_time > TIMEOUT:
                    raise TimeoutError("Remove edge word has hit timeout")
                
                if count > 10:  # If no more blacklist word found 10 times, return the final result
                    return words

                # Finding blacklist word in words and remove the blacklist word
                for word in blacklist_words:
                    if words[index] == word:
                        words.pop(index)
                    else:
                        count += 1   
        except Exception as e:
            system_log.error(f"Something went wrong: {e}")
            raise 

    
    try:
        # Looping throught every word in context and remove unused word
        for word in context.split():
            if word.lower() in unused_word:
                continue
            cleaned_word.append(word)

        # Remove blacklist word from the first word and merge into one str
        remove_first_word = remove_edge_word(not_first_word, cleaned_word, "first")
        temp_ctx = " ".join(w for w in remove_first_word)

        # Clean up the value of the time
        time_value = [temp_ctx.split()[-1], context.split()[-1]]
        temp_ctx = temp_ctx.replace(time_value[0], "").strip()

        # Remove blacklist word from the last word and merge into one str
        splited_temp_ctx = temp_ctx.split()
        remove_final_word = remove_edge_word(not_last_word, splited_temp_ctx, "last")
        cleaned_ctx = " ".join(w for w in remove_final_word)

        # Return the final context and time value
        return [cleaned_ctx, time_value[0], time_value[1]]
    except Exception as e:
        system_log.error(f"Something went wrong: {e}")


# Add the new reminder to the json
def set_reminder(context: str) -> None:
    try:
        # Clean up user input and get reminders.json data
        system_log.info("Setting new reminder")
        for i in [".", ","]:
            context = context.lower().replace(i, "")
        reminder_data = get_json_data()
        last_id = reminder_data["meta"]["last_id"]

        # Spliting context into reminder's context and time_value
        system_log.info("Cleaning context")
        cleaned_context = clean_context(context)
        context = cleaned_context[0]
        time_value = int(cleaned_context[1])
        time_unit = cleaned_context

        # Determine the time unit
        system_log.info("Set reminder time")
        if "second" in time_unit:
            reminder_time = datetime.now() + timedelta(seconds=time_value)
        elif "minute" in time_unit:
            reminder_time = datetime.now() + timedelta(minutes=time_value)
        elif "hour" in time_unit:
            reminder_time = datetime.now() + timedelta(hours=time_value)
        elif "day" in time_unit:
            reminder_time = datetime.now() + timedelta(days=time_value)    
        
        # Add new data to reminder_data
        reminder_data["meta"]["last_id"] += 1  # Update last id in json file
        reminder_data["reminders"][str(last_id + 1).zfill(3)] = {
            "context": cleaned_context,
            "time": reminder_time.isoformat(),
            "status": "pending"
        }
        
        # Add new reminder into json file
        add_json_data(reminder_path, reminder_data)
        return
    except Exception as e:
        system_log.error(f"Something went wrong while setting up the new reminder: {e}")
        raise


# Execute the reminder
def remind_me(tts_agent, interval: int) -> None:
    system_log.info("Start reminder module")
    try:
        # Looping every certain seconds to check the reminder json
        while True:
            reminders = get_json_data()
            now = datetime.now()

            # Checking each id from remind json file
            for rid in reminders["reminders"]:
                current_reminder = reminders["reminders"][rid]
                reminder_time = datetime.fromisoformat(current_reminder["time"])

                # If time now is pass the time in the reminder but not reminded yet
                if now >= reminder_time and current_reminder["status"] != "done":
                    reminder_ctx = current_reminder["context"]
                    isoed_time = reminder_time.isoformat()
                    
                    system_log.debug(f"Reminder for: {reminder_ctx}")
                    system_log.debug(f"Current time: {now.isoformat()}, Reminder time: {isoed_time}")
                    
                    # Updating reminder json file
                    reminders["reminders"][rid] = {
                        "context": reminder_ctx,
                        "time": isoed_time,
                        "status": "done"
                    }
                    add_json_data(reminder_path, reminders)

                    # Execute text-to-speech
                    choosen_template = random.choice(reminder_templates)
                    sentence = choosen_template.format(context=reminder_ctx)
                    voice_path = tts_agent.sylva_voice(sentence, "reminder.wav")
                    play_voice.play_sound(voice_path)

                    user_log.info(f"Sylva: {sentence}")
            # Sleep for interval time after check the json file
            time.sleep(interval)
    except Exception as e:
        system_log.error("Ending reminde me module")
        system_log.error(f"Something went wrong with remind me module: {e}")
        raise
