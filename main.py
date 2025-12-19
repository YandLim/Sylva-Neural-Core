# Importing modules and libraries
from utils import logger, tts_generator, play_voice
from core import stt, sylva_decision
from rasa.core.agent import Agent
from modules import greetings, get_time
from config import ex_config
import random
import time

# Define logger
system_log = logger.get_logger(__name__, system=True)
user_log = logger.get_logger(__name__, system=False)

# Getting model's path from config.py
nlu_model_path = ex_config.NLU_MODEL_PATH

# Important variabels
auto_sleep = 30
sylva_active = False
shutdown_pending = False
last_wake_time = 0
run_time = 0

# wake up Keyword and goodbye templates
wake_word = ["sylva", "wake up", "wakey wakey"]
sylva_templates = {
    "entering_sleep_mode": [
        "Standby mode engaged. Awaiting your next call, Master.",
        "No further input detected. Entering sleep state.",
        "Systems idle. Sylva will rest until summoned.",
        "Acknowledged. Transitioning to low-power mode.",
        "Silence confirmed. Entering sleep cycle now.",
        "All tasks complete. Sylva is going dormant.",
        "No commands received. Standing by in sleep mode.",
        "Power state reduced. Wake me when needed, Master.",
        "Monitoring paused. Sylva is now sleeping.",
        "Entering sleep mode. Systems will remain alert for wake signal."
    ],
    
    "goodbye_templates": [
        "Goodbye, Master. Sylva Standing by.",
        "Farewell, Sir. Until next activation.",
        "Session ending. Goodbye.",
        "Acknowledged. See you next time, Master.",
        "Sylva Going offline. Goodbye."
    ]
}

# Break module
def breaking_system():
    system_log.info("Shutdown Sylva system\n\n")
    farewell_phrase = random.choice(sylva_templates["goodbye_templates"])
    break_voice_path = tts.sylva_voice(farewell_phrase, "farewell.wav")
    play_voice.play_sound(break_voice_path)
    return True

# Main functionality
if __name__ == "__main__":
    try:
        # Load agents
        tts = tts_generator.SylvaTTSGenerator()
        nlu_agent = Agent.load(nlu_model_path)
        sylva_active = True

        # Generate log
        system_log.info("Activating model")
        user_log.info("Activating model")
        greetings.sylva_greet(tts)

        # Looping until user deactivate Sylva
        while True:
            run_time += 1
            # Speech to text function
            user_command = stt.speech_recognition()

            # Checking command avaiblity
            now = time.time()
            if user_command is not None:
                user_log.info(f"USER: {user_command}")

                # Check wake word in sleep mode
                if not sylva_active:
                    if any(w in user_command.lower() for w in wake_word):
                        # Activated Sylva
                        sylva_active = True 
                        last_wake_time = time.time()
                        system_log.info("Sylva entering active mode")

                        # Processing command 
                        if len(user_command.split(" ")) > 2:
                            if any(b_word in user_command.lower() for b_word in ["break", "brick", "brief"]):
                                break_status = breaking_system()
                                if break_status is True:
                                    break

                            sylva_decision.decision_making(tts, nlu_agent, user_command, shutdown_pending)
                        else:
                            greetings.sylva_greet(tts)

                        continue
                    else:
                        continue   # ignore everything in sleep mode

                # Update time
                last_wake_time = now

            # Prevent sleep on the first run
            if run_time == 1:
                last_wake_time = now

            # If timer is more than auto_sleep Sylva going down
            if now - last_wake_time > auto_sleep and run_time != 1 and sylva_active is True:
                random_sleep_phrase = random.choice(sylva_templates["entering_sleep_mode"])
                sleep_voice = tts.sylva_voice(random_sleep_phrase, "sleep.wav")
                play_voice.play_sound(sleep_voice)
                system_log.info("Sylva entering sleep mode")
                user_log.info(f"Sylva: {random_sleep_phrase}")
                sylva_active = False
                continue

            # Start proccessing commends
            if not user_command:
                continue

            if any(b_word in user_command.lower() for b_word in ["break", "brick", "brief"]):
                break_status = breaking_system()
                if break_status is True:
                    break

            # Update last wake time and do commands
            shutdown_pending = sylva_decision.decision_making(tts, nlu_agent, user_command, shutdown_pending)
            last_wake_time = time.time()
    except Exception as e:
        system_log.error(f"Something wen wrong while running the program: {e}\n\n")
