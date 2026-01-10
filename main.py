# Importing modules and libraries
from modules import greetings, remind_me, voice_input
from utils import logger, tts_generator
from core import stt, sylva_decision
from rasa.core.agent import Agent 
from config import ex_config
from threading import Thread
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
wake_word = ["sylva", "wake up", "wakey wakey", "silva", "silfa"]
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

# Breaking system module
def breaking_system() -> None:
    system_log.warning("Preparing to shutdown Sylva's system")
    farewell_phrase = random.choice(sylva_templates["goodbye_templates"])
    sylva_decision.execute_tts(tts_agent, farewell_phrase, "farewell.wav")
    system_log.warning("Shutdown Sylva system\n\n")
    return True

# Main functionality
if __name__ == "__main__":
    try:
        # Load agents
        tts_agent = tts_generator.SylvaTTSGenerator()
        nlu_agent = Agent.load(nlu_model_path)
        sylva_active = True

        # Generate log
        system_log.info("Activating model")
        user_log.info("Activating model")
        greeting_result = greetings.sylva_greet()
        sylva_decision.execute_tts(tts_agent, greeting_result.sentence, greeting_result.context)

        # Activate reminder threading
        system_log.info("Activating reminder thread")
        Thread(target=remind_me.remind_me, args=(tts_agent, 5,), daemon=True).start()

        # Asking confirmation for voice input module
        vcinput_confirmation = voice_input.vcinput_confirmation()
        sylva_decision.execute_tts(tts_agent, vcinput_confirmation.sentence, vcinput_confirmation.context)

        while True:
            user_decision = input(f"{vcinput_confirmation.sentence}(Y/n)\n=> ").lower()
            system_log.debug(f"User decision: {user_decision}")
            user_log.info(f"User: {user_decision}")
            if user_decision == "y":
                vcinput = voice_input.vcinput_confirm()
            elif user_decision == "n":
                vcinput = voice_input.vcinput_reject()
            else:
                print(f"{user_decision} is not Y or N")
                system_log.warning("User decision is not recognized")
                continue
            sylva_decision.execute_tts(tts_agent, vcinput.sentence, wav_ctx=vcinput.context)
            break

        # Looping until user deactivate Sylva
        while True:
            run_time += 1
            # Determine if the system use voice input module or text input module
            if vcinput.status is True:
                user_command = stt.speech_recognition()
            else:
                user_command = input("Master, Your Command: ")

            # Checking command availability
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

                            sylva_decision.decision_making(tts_agent, nlu_agent, user_command, shutdown_pending)
                        else:
                            module_result = greetings.sylva_greet()
                            sylva_decision.execute_tts(tts_agent, module_result.sentence, wav_ctx=module_result.context)

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
                sylva_decision.execute_tts(tts_agent, random_sleep_phrase, "sleep.wav")
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
            shutdown_pending = sylva_decision.decision_making(tts_agent, nlu_agent, user_command, shutdown_pending)
            last_wake_time = time.time()
    except Exception as e:
        system_log.error(f"Something went wrong while running the program: {e}\n\n")

    except KeyboardInterrupt:
        system_log.error(f"Keyboard interupting has detected. Turn of the system\n\n")
