"""This module is stand alone module, and use
for testing modules and function logic without using
TTS or STT."""

# Importing modules
from modules import greetings, get_time, get_date, shutdown, web_search, create_note, open_app, remind_me, voice_input
from utils import logger, play_voice, tts_generator
from utils.function_hint import TTSAgent
from typing import Optional

# Define system logger
testing_log = logger.get_logger(__name__, system=False, testing=True)

# Execute text to speech function
def execute_tts(tts_agent: TTSAgent, sentence: str, wav_ctx: str) -> None:
    testing_log.info("Executing text to speech function")
    wav_path = tts_agent.sylva_voice(sentence, f"{wav_ctx}.wav")
    play_voice.play_sound(wav_path)
    testing_log.debug(f"Sylva: {sentence}")
    return

# Sylva decision making functionality
def decision_making(
        intent: str,
        shutdown_pending: bool, 
        tts_agent: Optional[TTSAgent]=False, 
        value: Optional[str]=None, 
        user_command: Optional[str]=None 
    ) -> None:

    try:
        # shutdown_system confirmation
        if intent == "shutdown_system":
            testing_log.warning("Shutdown requested")
            shutdown_pending = shutdown.shutdown_confirmation()

            # Check if user use tts or not
            if tts_agent is not False:
                execute_tts(tts_agent, shutdown_pending.sentence, shutdown_pending.context)                
            return shutdown_pending.sentence

        if shutdown_pending:
            # Shutdown canceled
            if intent != "affirm":
                testing_log.info("Canceling shutdown module")
                shutdown_cancel = shutdown.shutdown_cancel(tts_agent)
                testing_log.info("Shutdown cancellation success")

                # Check if user use tts or not
                if tts_agent is not False:
                    execute_tts(tts_agent, shutdown_cancel.sentence, shutdown_cancel.context)              
                return shutdown_pending.sentence

            # Execute shutdown module
            else:
                testing_log.warning("Executing shutdown module")
                shutdown_approve = shutdown.shutdown_approval(tts_agent)    
                if tts_agent is not False:
                    execute_tts(tts_agent, shutdown_approve.sentence, shutdown_approve.context) 

                # Shutting down the system
                testing_log.warning("Execute shutdown system\n\n")
                shutdown.shutdown()

        # Decision list
        if intent == "greet":
            testing_log.info("Initializing greeting module")
            module_result = greetings.sylva_greet()
            testing_log.info("Greeting module complete. System standing by")

        elif intent == "get_time":
            testing_log.info("Initializing time module")
            module_result = get_time.current_time()
            testing_log.info("Time module complete. System standing by")

        elif intent == "get_date":
            testing_log.info("Initializing date module")
            module_result = get_date.current_date() 
            testing_log.info("Date module complete. System standing by")

        elif intent == "search_web":
            testing_log.info("Initializing web search module")
            module_result, search_result = web_search.search_result(value)
            
            # Check if user use tts or not
            if tts_agent is not False:
                execute_tts(tts_agent, module_result.sentence, module_result.context)
                execute_tts(tts_agent, search_result, module_result.context)
            else:
                testing_log.info(f"Output: {search_result}")

            testing_log.info("Web search module complete. System standing by")
            return
            
        
        elif intent == "note_create":
            testing_log.info("Initializing note module")
            module_result = create_note.create_note(value)
            testing_log.info("Note module complete. System standing by")
        
        elif intent == "open_app":
            testing_log.info("Opening application")
            module_result = open_app.run_module(value)
            testing_log.info("Open app module complete. Sylva standing by")
        
        elif intent == "remind_me":
            testing_log.info("Initializing reminder me module")
            module_result = remind_me.set_reminder(user_command)
            testing_log.info("Remind me module complete. System standing by")
            return
        
        # Check if user use tts or not
        if tts_agent is not False:
            execute_tts(tts_agent, module_result.sentence, module_result.context)
        else:
            testing_log.info(f"Output: {module_result.sentence}")
        return 
        
    except Exception as e:
        testing_log.error(f"Something went wrong while running module: {e}")
        raise

# The main testing function
def main():
    testing_log.info("Starting sylva testing mode")
    # Asking fro user's decision rather using text output or text output
    while True:
        vcoutput_confirmation = voice_input.vcinput_confirmation()
        user_decision = input(f"{vcoutput_confirmation.sentence}(Y/n)\n=> ").lower()

        # If user agree
        if user_decision == "y":
            vcoutput = voice_input.vcinput_confirm()
            tts_agent = tts_generator.SylvaTTSGenerator()
            execute_tts(tts_agent, vcoutput.sentence, wav_ctx=vcoutput.context)

        # If user not agree
        elif user_decision == "n":
            vcoutput = voice_input.vcinput_reject()
            testing_log.info(f"Sylva: {vcoutput.sentence}")

        # If user halucinate
        else:
            print(f"{user_decision} is not Y or N")
            testing_log.warning("User decision is not recognized")
            continue
        break
    
    # Looping to test modules, until user type break
    while True:
        # The currently available commands     
        print("""
            Sylva's Commands and how to trigger:
            - Greetings(greet)
            - Get time(get_time)
            - Get date(get_date)
            - Search web(search_web)
            - Create note(note_create)
            - Open app(open_app)
            - reminde me(remind_me)
            - shutdown(shutdown_system)
            - break"""
        )

        # Asking for user command
        user_command = input("What is the command: ").lower()
        for command in user_command.split():  # Checking for user command
            found = True
            breaked = False

            # Basic command without value needed
            if command == "greet" or command == "get_time" or command == "get_date":
                decision_making(command, False, tts_agent=tts_agent if vcoutput.status is True else False)
            
            # Comment that need value
            elif command == "search_web" or command == "note_create" or command == "open_app":
                value = input("Enter the value: ")
                decision_making(command, False, tts_agent=tts_agent if vcoutput.status is True else False, value=value)

            elif command == "remind_me":
                value = input("What time and what is the reminder context: ")
                decision_making(command, False, tts_agent=tts_agent if vcoutput.status is True else False, user_command=value)

            # Shutdown command
            elif command == "shutdown_system":
                shutdown_pending = decision_making(command, False, tts_agent=tts_agent if vcoutput.status is True else False)
                user_decision = input(f"{shutdown_pending}(Y/n): ").lower()

                if user_decision == "y":
                    decision_making("affirm", True, tts_agent=tts_agent if vcoutput.status is True else False)
                else:
                    decision_making("deny", True, tts_agent=tts_agent if vcoutput.status is True else False)

            # If user want to end the system
            elif command == "break":
                breaked = True
                return
            
            else:
                found = False
        
        # If no command is found
        if found is False:
            if breaked is True:
                break

            print(f"User input: {user_command} doesn't contains any command")

if __name__ == "__main__":
    main()
        
