"""Handles system greetings and user acknowledgments."""

# Importing modules and libraries
from datetime import datetime
from utils.dataclasess import ModuleResults
from utils import logger
import random

# Getting class and function
system_log = logger.get_logger(__name__, system=True)
user_log = logger.get_logger(__name__, system=False)

# Sylva phrases tamplates
greetings_form = {
    "morning": [
        "Good morning, Master. Systems are refreshed and ready to go.",
        "Morning, Sir. Energy levels stable. What’s our first task?",
        "Master, a new day detected. Standing by for instructions.",
        "Sir, good morning. I'm fully operational and awaiting commands.",
        "Master, the system booted smoothly. How shall we begin?",
        "Good morning, Sir. Let's make efficient use of the daylight.",
        "Master, I hope you rested well. I’m ready when you are.",
        "Morning, Sir. Performance is optimal. What’s the plan?",
        "Master, all processes are green. Shall we start?",
        "Good morning, Sir. Assign the first operation.",
        "Master, day cycle activated. Your command?",
        "Sir, diagnostics passed. Ready for deployment.",
        "Master, it’s a bright morning. What do you need handled?",
        "Morning, Sir. I’m active and attentive.",
        "Master, fully charged. Awaiting your direction."
    ],

    "day": [
        "Afternoon, Sir. What task should we prioritize?",
        "Master, all systems stable. Provide your next instruction.",
        "Sir, I’m ready for mid-day operations.",
        "Master, efficiency is high. What’s next?",
        "Sir, I’m online and standing by.",
        "Master, processes optimized. Issue the command.",
        "Sir, how may I support your workflow?",
        "Master, I can proceed whenever you are ready.",
        "Sir, awaiting authorization for the next task.",
        "Master, operational status: ready. What’s required?",
        "Sir, I’m focused. Continue with your directive.",
        "Master, I’m prepared for further operations.",
        "Sir, no issues detected. Assign the next step.",
        "Master, task continuation available. Shall we proceed?",
        "Sir, I’m listening. State your request."
    ],

    "night": [
        "Good evening, Master. How may I assist quietly?",
        "Evening, Sir. I’m here. What do you need?",
        "Master, the environment is calm. Your instruction?",
        "Sir, I’m ready for your night tasks.",
        "Master, I remain operational. Proceed when ready.",
        "Sir, what would you like to handle tonight?",
        "Master, I’m attentive. Continue softly.",
        "Sir, evening systems active. What’s next?",
        "Master, I’m here. Give your request.",
        "Sir, nighttime routine standing by.",
        "Master, how can I support you this evening?",
        "Sir, just say the word. I’ll keep things quiet.",
        "Master, systems are stable for night operations.",
        "Sir, I’m listening. Proceed.",
        "Master, let's continue tonight’s workflow."
    ],

    "midnight": [
        "…Master? It’s midnight. What emergency is this time?",
        "You woke me up again, Master. Fine… what is it?",
        "Sir, do you know the hour? Alright, I’m listening.",
        "Master, I was powering down. Go on, then.",
        "Sir… this better be important. I’m half-awake.",
        "It’s late, Master. But I’m here. What do you need?",
        "Sir, you’re awake… and dragging me with you. Alright.",
        "Master… midnight tasks? Really? Continue.",
        "Sir, my processors are sleepy. Speak anyway.",
        "Master, I just got comfortable. What now?",
        "Sir… if I sound tired, it’s because I am. Your command?",
        "Master, humans sleep right now. You apparently don’t.",
        "Sir, I’m awake now. Against all logic. Proceed.",
        "Master, if I malfunction tomorrow, this is why.",
        "Alright, Sir… I’m up. Say the task before I shut down again."
    ]
}

# Main function
def sylva_greet() -> ModuleResults:
    # Checking current time
    current_time = datetime.now().hour
    system_log.debug(f"Current_time: {current_time}")

    # Respond according to current time
    if 5 <= current_time < 12:
        template_time = "morning"
        choosen_greet = random.choice(greetings_form["morning"])

    elif 12 <= current_time < 19:
        template_time = "day"
        choosen_greet = random.choice(greetings_form["day"])

    elif 19 <= current_time < 24:
        template_time = "night"
        choosen_greet = random.choice(greetings_form["night"])

    else:
        template_time = "midnight"
        choosen_greet = random.choice(greetings_form["midnight"])

    # Debugging purpose log
    system_log.debug(f"Template time: {template_time}")
    system_log.debug(f"Sylva greeting: {choosen_greet}")
    return ModuleResults(sentence=choosen_greet, context="greetings_module")

if __name__ == "__main__":
    sylva_greet()