# Importing modules
from modules import greetings, get_time, get_date, shutdown, web_search, create_note, open_app, remind_me
from utils.function_hint import TTSAgent, NLUAgent
from utils import logger, play_voice
from core import intent_processor
import asyncio

# Define system logger
system_log = logger.get_logger(__name__, system=True)
user_log = logger.get_logger(__name__, system=False)

# Execute text to speech function
def execute_tts(tts_agent: TTSAgent, sentence: str, wav_ctx: str) -> None:
    system_log.info("Executing text to speech function")
    wav_path = tts_agent.sylva_voice(sentence, f"{wav_ctx}.wav")
    play_voice.play_sound(wav_path)
    user_log.info(f"Sylva: {sentence}")
    return

# Sylva decision making functionality
def decision_making(tts_agent: TTSAgent, nlu_agent: NLUAgent, user_command: str, shutdown_pending: bool) -> None:
    try:
        # Running natural language understanding
        intent, value = asyncio.run(intent_processor.running_model(nlu_agent, user_command))

        # shutdown_system confirmation
        if intent == "shutdown_system":
            system_log.warning("Shutdown requested")
            shutdown_pending = shutdown.shutdown_confirmation()
            execute_tts(tts_agent, shutdown_pending.sentence, shutdown_pending.context)
            return

        if shutdown_pending:
            # Shutdown canceled
            if intent != "affirm":
                system_log.info("Canceling shutdown module")
                shutdown_cancel = shutdown.shutdown_cancel(tts_agent)
                system_log.info("Shutdown cancellation success")

                execute_tts(tts_agent, shutdown_cancel.sentence, shutdown_cancel.context)
                return

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

        elif intent == "get_time":
            system_log.info("Initializing time module")
            module_result = get_time.current_time()
            system_log.info("Time module complete. System standing by")

        elif intent == "get_date":
            system_log.info("Initializing date module")
            module_result = get_date.current_date() 
            system_log.info("Date module complete. System standing by")

        elif intent == "search_web":
            system_log.info("Initializing web search module")
            module_result, search_result = web_search.search_result(value)

            execute_tts(tts_agent, module_result.sentence, module_result.context)
            execute_tts(tts_agent, search_result, module_result.context)

            system_log.debug(f"Search result: {search_result}")
            user_log.info(f"Search result: {search_result}")

            system_log.info("Web search module complete. System standing by")
            return
        
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
        
        else:
            system_log.debug(f"User command: {e}")
            system_log.debug("User command can't be understand")
            return
        
        # Execute text to speech from ran module
        execute_tts(tts_agent, module_result.sentence, module_result.context)
        return 
        
    except Exception as e:
        system_log.error(f"Something went wrong while running module: {e}")
        raise
    