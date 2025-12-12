# Importing modules
from modules import greetings, get_time, get_date, shutdown, web_search, create_note
from utils import logger
from core import intent_processor
import asyncio

# Define system logger
log = logger.get_logger(__name__)

# Sylva decision making functionality
def decision_making(tts_agent, nlu_agent, user_command, shutdown_pending):
    # Running natural language understanding
    intent, value = asyncio.run(intent_processor.running_model(nlu_agent, user_command))

    # shutdown_system confirmation
    if intent == "shutdown_system":
        shutdown_pending = shutdown.shutdown_confirmation(tts_agent)
        log.warning("Shutdown requested")
        return shutdown_pending

    if shutdown_pending:
        # Shutdown canceled
        if intent != "affirm":
            log.info("Canceling shutdown process")
            shutdown_pending = shutdown.shutdown_cancel(tts_agent)

        # Execute shutdown module
        else:
            log.info("Executing shutdown process")
            shutdown.shutdown_approval(tts_agent)    

    # Decision list
    if intent == "greet":
        log.info("Sylva greeting")
        greetings.sylva_greet(tts_agent)
        return

    elif intent == "get_time":
        log.info("Sylva sychronize with clock")
        get_time.current_time(tts_agent)
        return

    elif intent == "get_date":
        log.info("Sylva synchronize with calender")
        get_date.current_date(tts_agent)   
        return 

    elif intent == "search_web":
        log.info(f"Searching web for: {value}")
        web_search.search_result(value, tts_agent)
        return
    
    elif intent == "note_create":
        log.info("Sylva writing down...")
        create_note.create_note(tts_agent, value)
        return