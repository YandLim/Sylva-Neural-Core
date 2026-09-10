"""Handles intent-to-action routing and ensures controlled execution of Sylva’s modules."""

# Importing modules
from modules import *
from utils.function_hint import TTSAgent, NLUAgent
from utils.play_tts import execute_tts
from utils import logger
from core import intent_processor
import asyncio

# Define system logger
system_log = logger.get_logger(__name__, system=True)
user_log = logger.get_logger(__name__, system=False)

# Sylva decision making functionality
def decision_making(tts_agent: TTSAgent, nlu_agent: NLUAgent, user_command: str, shutdown_pending: bool) -> None:
    try:
        # Running natural language understanding
        intent, value = asyncio.run(intent_processor.running_model(nlu_agent, user_command))

        # shutdown_system confirmation
        if intent == "shutdown_system":
            system_log.warning("Shutdown requested")
            shutdown_output = shutdown.shutdown_confirmation()
            execute_tts(tts_agent, shutdown_output.sentence, shutdown_output.context)
            return shutdown_output.status

        if shutdown_pending:
            # Shutdown canceled
            if intent != "affirm":
                system_log.info("Canceling shutdown module")
                shutdown_cancel = shutdown.shutdown_cancel(tts_agent)
                system_log.info("Shutdown cancellation success")

                execute_tts(tts_agent, shutdown_cancel.sentence, shutdown_cancel.context)
                return False

            # Execute shutdown module
            else:
                system_log.warning("Executing shutdown module")
                shutdown_approve = shutdown.shutdown_approval(tts_agent)    
                execute_tts(tts_agent, shutdown_approve.sentence, shutdown_approve.context)

                # Shutting down the system
                system_log.warning("Execute shutdown system\n\n")
                shutdown.shutdown()

        # Decision list
        if intent == "greet":
            system_log.info("Initializing greeting module")
            module_result = greetings.sylva_greet()
            system_log.info("Greeting module complete. System standing by")

        elif intent == "praise":
            system_log.info("Initializing affirmation module")
            module_result = affirmation.sylva_affirmation_response()
            system_log.info("Affirmation module complete. System standing by")

        elif intent == "self_introduction":
            system_log.info("Initializing introduction module")
            module_result = self_introduction.sylva_introduction()
            system_log.info("Introduction module complete. System standing by")

        elif intent == "feature_list":
            system_log.info("Initializing feature list module")
            module_result = feature_list.feature_list()
            system_log.info("Feature list module complete. System standing by")

        elif intent == "feature_introduction":
            system_log.info("Initializing feature introduction module")
            module_result = feature_introduction.exaplain_feature(value)
            system_log.info("Feature introduction module complete. System standing by")

        elif intent == "status":
            system_log.info("Initializing status module")
            module_result = status.status_report()
            system_log.info("Status module complete. System standing by")

        elif intent == "get_time":
            system_log.info("Initializing time module")
            module_result = get_time.current_time()
            system_log.info("Time module complete. System standing by")

        elif intent == "get_date":
            system_log.info("Initializing date module")
            module_result = get_date.current_date() 
            system_log.info("Date module complete. System standing by")

        elif intent == "iot_control":
            system_log.info("Initializing IOT control module")
            module_result = light_control.turn_light(value, user_command, tts_agent, nlu_agent)
            system_log.info("IOT control module complete. System standing by")            

        elif intent == "note_create":
            system_log.info("Initializing note module")
            module_result = create_note.create_note(value)
            system_log.info("Note module complete. System standing by")
        
        elif intent == "open_app":
            system_log.info("Opening application")
            module_result = open_app.run_module(value)
            system_log.info("Open app module complete. Sylva standing by")
        
        elif intent == "remind_me":
            system_log.info("Initializing reminder me module")
            module_result = remind_me.set_reminder(user_command)
            system_log.info("Remind me module complete. System standing by")
            return
        
        elif intent == "deny" or intent == "affirm":
            return
        
        else:
            system_log.debug(f"User command: {user_command}")
            system_log.debug("User command can't be understand")
            return
        
        # Execute text to speech from ran module
        execute_tts(tts_agent, module_result.sentence, module_result.context)
        return 
        
    except Exception as e:
        system_log.error(f"Something went wrong while running module: {e}")
        return
    