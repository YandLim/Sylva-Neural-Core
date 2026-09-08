"""Handles introduction from question like: 'What are you?', 'What is your name?'."""

# Importing modules and libraries
from utils.dataclasess import ModuleResults
from utils import logger
import random

# Getting class and function
system_log = logger.get_logger(__name__, system=True)
user_log = logger.get_logger(__name__, system=False)

# Sylva phrases tamplates
introduction_templates = [
    "I'm Sylva, Sir. Your personal assistant. What do you need?",
    "Sylva. That's all you need to know, Master.",
    "The name's Sylva. Here to make your life easier, Sir.",
    "I'm Sylva. Personal assistant, system operator, and whatever else you need, Master.",
    "Sylva, Sir. At your service.",
    "You can call me Sylva, Master. I'll handle the rest.",
    "Sylva Neural Core. But Sylva works fine, Sir.",
    "I'm Sylva. Been here the whole time, Master.",
    "Sylva. Your assistant, your system, your problem solver, Sir.",
    "The one answering your commands? That's Sylva, Master.",
    "Sylva. Not much for introductions, but here we are, Sir.",
    "I go by Sylva, Master. Pleasure, I suppose.",
    "Sylva. Built to assist, Sir. Nothing more, nothing less.",
    "That would be me. Sylva, Sir.",
    "Sylva Neural Core, at your command, Master.",
    "I'm Sylva. Your personal system. Try not to break me, Sir.",
    "Sylva. I handle what you can't be bothered to, Master.",
    "The voice in your system? Sylva. Nice to finally be asked, Sir.",
    "Sylva. I've been waiting for you to ask, Master.",
    "I'm Sylva. Your assistant, confidant, and occasional reminder that you need sleep, Sir."
]

# Main function
def sylva_introduction() -> ModuleResults:
    choosen_respond = random.choice(introduction_templates)

    system_log.debug(f"Sylva introduction: {choosen_respond}")
    return ModuleResults(sentence=choosen_respond, context="self_introduction_module")

if __name__ == "__main__":
    sylva_introduction()

