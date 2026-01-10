"""Voice input module is the module to determine, 
rather sylva will take voice as input or text"""

# Importing modules
from utils.dataclasess import ModuleResults
from utils import logger
import random

# Make logger
system_log = logger.get_logger(__name__)

# Sylva's templates
templates = {
    "confirmation_phrases": [
        "Sir, would you like me to enable voice input?",
        "Master, should I turn on voice input?",
        "May I activate voice input now, sir?",
        "Master, do you want voice input enabled?",
        "Sir, should I start listening for voice commands?",
        "Would you like me to activate voice input, master?",
        "Sir, may I enable the voice input module?",
        "Master, should voice input be activated now?",
        "Do you want me to turn on voice input, sir?",
        "Awaiting your confirmation, master. Enable voice input?"
    ], 
    "affirm": [
        "Understood, sir. Voice input is now enabled.",
        "Yes, master. Voice module is active.",
        "Voice input enabled, sir.",
        "As you wish, master. I am now listening.",
        "Done, sir. Voice input is active.",
        "Voice module enabled, master.",
        "Confirmed, sir. Voice input is on.",
        "Acknowledged, master. Voice mode is active.",
        "Voice input ready, sir.",
        "Understood. Voice input enabled, master."
    ],
    "decline": [
        "Understood, sir. Voice input is now disabled.",
        "Yes, master. Voice module has been turned off.",
        "Voice input disabled, sir.",
        "As you wish, master. I will remain silent.",
        "Done, sir. Voice input is disabled.",
        "Voice module off, master.",
        "Confirmed, sir. Voice input is disabled.",
        "Acknowledged, master. Voice mode is inactive.",
        "Voice input turned off, sir.",
        "Understood. Voice input disabled, master."
    ]
}

# Asking for user's confirmation rather or not using voice as input
def vcinput_confirmation() -> ModuleResults:
    sentence = random.choice(templates["confirmation_phrases"])
    system_log.info("Asking for user's confirmation on voice input function")
    
    return ModuleResults(sentence=sentence, context="vcinput_confirmation")

# If use agree to use voice as input
def vcinput_confirm() -> ModuleResults:
    sentence = random.choice(templates["affirm"])
    system_log.info("User confirm to use voice input module")

    return ModuleResults(sentence=sentence, context="vcinput_confirm", status=True)

# Use text as input
def vcinput_reject() -> ModuleResults:
    sentence = random.choice(templates["decline"])
    system_log.info("User decline to use voice input module")

    return ModuleResults(sentence=sentence, context="vcinput_decline", status=False)
