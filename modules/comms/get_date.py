"""Allows Sylva to perceive the current date."""

# Importing modules
from utils.dataclasess import ModuleResults
from datetime import datetime
from utils import logger
import random

# Define class
system_log = logger.get_logger(__name__, system=True)
user_log = logger.get_logger(__name__, system=False)

# Sylva phrases tamplates
date_templates = [
    "Today's date is {date}, Sir.",
    "Master, the current date is {date}.",
    "System calendar reads {date}.",
    "The date today is {date}.",
    "Sir, according to my calendar, it's {date}.",
    "Date verification complete. It's {date}.",
    "Master, today’s full date is {date}.",
    "Current date detected: {date}.",
    "It's {date}, Sir.",
    "My calendar module reports {date}.",
    "We are currently on {date}, Master.",
    "Today is {date}.",
    "Sir, the date is {date}.",
    "Master, system confirms the date: {date}.",
    "Calendar check complete. It's {date}.",
    "I read the date as {date}, Sir.",
    "The official date today is {date}.",
    "My internal clock marks today as {date}.",
    "Master, today registers as {date}.",
    "It is {date}, Sir."
]

# Main date function
def current_date() -> ModuleResults:
    # Get date
    cur_date = datetime.now().strftime("%A, %d %B %Y")
    system_log.debug(f"Date: {cur_date}")

    # Choose template
    choosen_template = random.choice(date_templates)
    sentence = choosen_template.format(date=cur_date) 
    
    return ModuleResults(sentence=sentence, context="get_date_module")

if __name__ == "__main__":
    current_date()