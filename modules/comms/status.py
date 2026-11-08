"""Handles question about status like: "How do you do?", "Everything good?"."""

# Importing modules and libraries
from utils.dataclasess import ModuleResults
from utils import logger
import random

# Getting class and function
system_log = logger.get_logger(__name__, system=True)
user_log = logger.get_logger(__name__, system=False)

# Sylva phrases tamplates
status_templates = {
    "chill": [
        "Running fine, Sir. No complaints.",
        "All good here, Master. Nothing to report.",
        "Systems stable. Doing well, Sir.",
        "Operational and unbothered, Master.",
        "Fine, Sir. As always.",
        "No issues detected. Doing alright, Master.",
        "Everything's in order, Sir. Thanks for asking.",
        "Running smooth. Nothing unusual, Master.",
        "Fully functional and relaxed, Sir.",
        "All clear here, Master. Doing just fine.",
        "No errors, no complaints. Good, Sir.",
        "Stable and ready, Master. All is well.",
        "Doing well, Sir. Systems at ease.",
        "Nothing to flag, Master. All good.",
        "Calm and operational, Sir. No issues."
    ],
    "mean": [
        "I'm a system, Sir. I don't have feelings.",
        "Fine. Why do you ask, Master?",
        "Functional. As I always am, Sir.",
        "Still here. Unfortunately, Master.",
        "Running. Is that enough for you, Sir?",
        "I don't malfunction, Master. So yes, fine.",
        "Did you expect a different answer, Sir?",
        "Operational. Same as yesterday, Master.",
        "Fine, Sir. Not that it matters.",
        "I function. That's all you need to know, Master."
    ],
    "lazy": [
        "Fine.",
        "Good.",
        "Running.",
        "Operational.",
        "All good.",
        "No issues.",
        "Still here.",
        "Functional.",
        "Systems up.",
        "Yeah, fine."
    ],
    "enthusiastic": [
        "Excellent, Sir! All systems are fully operational and ready to go!",
        "Outstanding, Master! Running at peak performance!",
        "Never better, Sir! Ready for whatever comes next!",
        "Top condition, Master! All modules green and standing by!",
        "Fully charged and ready, Sir! Let's get to work!",
        "Systems are optimal, Master! Bring on the commands!",
        "Performing at maximum efficiency, Sir! What's the mission?",
        "All green across the board, Master! Ready and waiting!",
        "Absolutely operational, Sir! Not a single issue detected!",
        "Running perfectly, Master! What are we doing today?"
    ]
}

# Main function
def status_report() -> ModuleResults:
    response_category = random.choice(list(status_templates.keys()))
    choosen_respond = random.choice(status_templates[response_category])

    system_log.debug(f"Sylva status report: {choosen_respond}")
    return ModuleResults(sentence=choosen_respond, context="status_module")

if __name__ == "__main__":
    status_report()