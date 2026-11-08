"""Grants Sylva authority to terminate system operations."""

# Importing modules
from utils.dataclasess import ModuleResults
from utils import logger, play_voice
from utils.function_hint import TTSAgent
import random
import os

# Defining class
system_log = logger.get_logger(__name__, system=True)

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

    "shutdown_approve": [
        "Understood, Master. Shutting down in {seconds} seconds. Farewell.",
        "Command accepted, Sir. Powering off in {seconds} seconds. Until next cycle.",
        "Affirmative. System will deactivate in {seconds} seconds. Rest well, Master.",
        "Approval logged. Sylva will go offline in {seconds} seconds. Goodbye.",
        "Master, termination confirmed. Power down in {seconds} seconds. I await your return.",
        "Deactivation sequence initiated. System halts in {seconds} seconds. Farewell, Sir.",
        "Acknowledged. Full shutdown in {seconds} seconds. Standing by for the next activation.",
        "Master, all processes closing in {seconds} seconds. Safe to disconnect. Goodbye.",
        "Command received. Entering shutdown mode in {seconds} seconds. Until you call again.",
        "Sir, final sequence engaged. Power drops in {seconds} seconds. Farewell for now."
    ]
}

# Confirming decision
def shutdown_confirmation() -> ModuleResults:
    confirmation_phrase = random.choice(shutdown_dialogues["shutdown_confirmation"])
    system_log.warning("Sylva asked for shutdown approval")

    # Turn on shutdown process
    return ModuleResults(sentence=confirmation_phrase, context="shutdown_confirmation", status=True)


# Shutdown confimed
def shutdown_approval(tts_agent: TTSAgent) -> ModuleResults:
    confirm_phrase = random.choice(shutdown_dialogues["shutdown_approve"])
    phrase_format = confirm_phrase.format(seconds="10")
    system_log.warning("User approved the shutdown process")
    return ModuleResults(phrase_format, context="shutdown_approve")

def shutdown():
        os.system("shutdown /s /t 10")


# Shutdown canceled
def shutdown_cancel(tts_agent: TTSAgent) -> ModuleResults:
    sentence = random.choice(shutdown_dialogues["shutdown_cancel"])
    system_log.warning("User canceled shutdown process")
    return ModuleResults(sentence=sentence, context="shutdown_cancel", status=False)
