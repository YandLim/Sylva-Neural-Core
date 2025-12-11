"""Give Sylva access to shutdown the system"""

# Importing modules
from utils import logger, play_voice
import random
import os

# Defining class
log = logger.get_logger(__name__)

# Sylva phrases tamplates
shutdown_dialogues = {
    "shutdown_confirmation": [
        "Sir, to confirm, do you wish to terminate my systems?",
        "Master, should I proceed with the shutdown sequence?",
        "Confirming request: do you want Sylva to power down?",
        "Before I deactivate, Sir, please confirm the shutdown command.",
        "Master, I require your confirmation to begin system termination.",
        "Sir, shall I initiate the shutdown protocol?",
        "To proceed, Master, I need your verbal confirmation.",
        "Shutdown command detected. Do you want me to continue?",
        "Sir, please confirm if system deactivation is intended.",
        "Master, awaiting your approval to end current operations."
    ],

    "shutdown_approve": [
        "Acknowledged, Sir. Ending processes now. Goodbye.",
        "Shutdown confirmed. It was a privilege assisting you, Master.",
        "Command accepted. Powering down. Rest well, Sir.",
        "Understood, Master. Deactivating… see you next cycle.",
        "Your approval is received. Sylva is shutting down.",
        "All systems closing. Farewell, Sir.",
        "Master, termination confirmed. Entering full shutdown.",
        "Thank you for today. Powering off now, Sir.",
        "Approval logged. Ending operation sequence. Goodbye.",
        "Master, shutting down. I will await your next activation."
    ],

    "shutdown_cancel": [
        "Shutdown aborted, Sir. Systems remain active.",
        "Cancellation received. I’ll stay online, Master.",
        "Understood. I won't power down.",
        "Shutdown sequence halted. Standing by for further tasks.",
        "Alright, Sir. Remaining operational.",
        "Deactivation cancelled. What would you like next, Master?",
        "Shutdown stopped. I am still here.",
        "Command reversed. Maintaining full functionality.",
        "Acknowledged. Sylva will not shut down.",
        "Master, request withdrawn. I remain at your service."
    ],

    "shutdown_countdown": [
        "Shutdown sequence initiated. Powering off in {seconds} seconds, Sir.",
        "Master, system termination begins now. {seconds} seconds until full shutdown.",
        "Final notice: shutdown will occur in {seconds} seconds. Prepare accordingly.",
        "Beginning power-down countdown. {seconds} seconds until deactivation, Sir.",
        "Shutdown confirmed. The system will go offline in {seconds} seconds.",
        "Master, deactivation is imminent. {seconds} seconds until all processes stop.",
        "Alert: Sylva will shut down in {seconds} seconds. No further input required.",
        "Command accepted. Power will drop in {seconds} seconds. Standing by for silence.",
        "Executing shutdown protocol. {seconds} seconds until complete system halt.",
        "Sir, this is your final countdown. System will shut down in {seconds} seconds."
    ]
}

# Confirming decision
def shutdown_confirmation(tts_agent):
    confirmation_phrase = random.choice(shutdown_dialogues["shutdown_confirmation"])
    confirmation = tts_agent.sylva_voice(confirmation_phrase, "shutdown_confirmation.wav")
    play_voice.play_sound(confirmation)

    log.debug("Sylva asked for shutdown approval")
    return True # Turn on shutdown process


# Shutdown confimed
def shutdown_approval(tts_agent):
    confirm_phrase = random.choice(shutdown_dialogues["shutdown_approve"])
    approve = tts_agent.sylva_voice(confirm_phrase, "shutdown_approve.wav")
    play_voice.play_sound(approve)
    log.debug("User approved the shutdown process")

    # Start countdown
    countdown_phrase = random.choice(shutdown_dialogues["shutdown_countdown"])
    countdown_format = countdown_phrase.format(seconds="15")
    countdown = tts_agent.sylva_voice(countdown_format, "shutdown_countdown.wav")
    play_voice.play_sound(countdown)

    # Shutting down the system
    log.warning("Execute shutdown system\n\n")
    os.system("shutdown /s /t 10")
    return


# Shutdown canceled
def shutdown_cancel(tts_agent):
    cancel_phrase = random.choice(shutdown_dialogues["shutdown_cancel"])
    cancel = tts_agent.sylva_voice(cancel_phrase, "shutdown_cancel.wav")
    play_voice.play_sound(cancel)

    log.debug("User canceled shutdown process")
    return False # Turn of shutdown process
