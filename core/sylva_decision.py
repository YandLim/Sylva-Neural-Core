# Importing modules
from modules import greetings, get_time, get_date, shutdown, web_search, create_note, open_app
from utils import logger
from core import intent_processor
import asyncio

# Define system logger
system_log = logger.get_logger(__name__, system=True)

# Sylva decision making functionality
def decision_making(tts_agent, nlu_agent, user_command, shutdown_pending):
    # Running natural language understanding
    intent, value = asyncio.run(intent_processor.running_model(nlu_agent, user_command))

    # shutdown_system confirmation
    if intent == "shutdown_system":
        system_log.warning("Shutdown requested")
        shutdown_pending = shutdown.shutdown_confirmation(tts_agent)
        return shutdown_pending

    if shutdown_pending:
        # Shutdown canceled
        if intent != "affirm":
            system_log.info("Canceling shutdown module")
            shutdown_pending = shutdown.shutdown_cancel(tts_agent)
            system_log.info("Shutdown cancellation success")

        # Execute shutdown module
        else:
            system_log.warning("Executing shutdown module")
            shutdown.shutdown_approval(tts_agent)    

    # Decision list
    if intent == "greet":
        system_log.info("Initializing greeting module")
        greetings.sylva_greet(tts_agent)
        system_log.info("Greeting module complete. System standing by")
        return

    elif intent == "get_time":
        system_log.info("Initializing time module")
        get_time.current_time(tts_agent)
        system_log.info("Time module complete. System standing by")
        return

    elif intent == "get_date":
        system_log.info("Initializing date module")
        get_date.current_date(tts_agent) 
        system_log.info("Date module complete. System standing by")
        return 

    elif intent == "search_web":
        system_log.info("Initializing web search module")
        web_search.search_result(value, tts_agent)
        system_log.info("Web search module complete. System standing by")
        return
    
    elif intent == "note_create":
        system_log.info("Initializing note module")
        create_note.create_note(tts_agent, value)
        system_log.info("Note module complete. System standing by")
        return
    
    elif intent == "open_app":
        system_log.info("Opening application")
        open_app.run_module(tts_agent, value)
        system_log.info("Open app module complete. Sylva standing by")
        return
    