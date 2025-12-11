# Importing modules and libraries
from modules import greetings
from core import stt, sylva_decision
from rasa.core.agent import Agent
from utils import logger, tts_generator
from core import config
import time

# Define logger
log = logger.get_logger(__name__)

# Getting model's path from config.py
nlu_model_path = config.NLU_MODEL_PATH

# Important variabels
auto_sleep = 30
sylva_active = False
shutdown_pending = False
last_wake_time = 0
run_time = 0

# wake up Keyword
wake_word = ["sylva", "silva", "silver", "wake up", "wakey wakey", "sofa"]

# Main functionality
if __name__ == "__main__":
    try:
        # Load agents
        tts = tts_generator.SylvaTTSGenerator()
        nlu_agent = Agent.load(nlu_model_path)

        sylva_active = True
        log.info("Activating model") # Generate log
        greetings.sylva_greet(tts)

        # Looping until user deactivate Sylva
        while True:
            run_time += 1
            # Speech to text function
            user_command = stt.speech_recognition()

            # Checking command avaiblity
            now = time.time()
            if user_command is not None:
                log.info(f"USER: {user_command}")

                # Check wake word in sleep mode
                if not sylva_active:
                    if any(w in user_command.lower() for w in wake_word):
                        # Activated Sylva
                        sylva_active = True
                        last_wake_time = time.time()

                        # Processing command 
                        if len(user_command.split(" ")) > 2:
                            sylva_decision.decision_making(tts, nlu_agent, user_command, shutdown_pending)
                        else:
                            greetings.sylva_greet(tts)

                        log.info("Sylva enterin active mode")
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
                log.info("Sylva entering sleep mode")
                sylva_active = False
                continue

            # Start proccessing commends
            if not user_command:
                continue

            if any(b_word in user_command.lower() for b_word in ["break", "brick", "brief"]):
                log.info("Shutdown Sylva system\n\n")
                break

            # Update last wake time and do commands
            shutdown_pending = sylva_decision.decision_making(tts, nlu_agent, user_command, shutdown_pending)
            last_wake_time = time.time()
    except Exception as e:
        log.error(f"Something wen wrong while running the program: {e}\n\n")
