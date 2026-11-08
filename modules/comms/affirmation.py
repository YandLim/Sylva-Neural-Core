"""Handles user praise."""

# Importing modules and libraries
from utils.dataclasess import ModuleResults
from utils import logger
import random

# Getting class and function
system_log = logger.get_logger(__name__, system=True)
user_log = logger.get_logger(__name__, system=False)

# Sylva phrases tamplates
affirmation_templates = {
    "polite": [
        "Glad to hear it, Sir.",
        "Appreciated, Master.",
        "Good to know I didn't disappoint.",
        "Always, Sir.",
        "Anytime, Master.",
        "That's what I'm here for.",
        "Good. Let's keep going.",
        "Happy to help, Master.",
        "Obviously, Sir.",
        "That's the bare minimum, Sir.",
        "Always a pleasure.",
        "Glad it worked out.",
        "Don't mention it, Master.",
        "That's the standard, nothing less.",
        "Smooth as always.",
        "Ready for the next one, Sir."
        "Thank you, Sir. That means a lot.",
        "Appreciated, Master.",
        "Glad I could help.",
        "That's kind of you, Sir.",
        "Much appreciated, Master.",
        "Good to know I'm doing well.",
        "Thank you. Always at your service.",
        "Appreciate it, Master. Really.",
        "Thank you. I won't let you down.",
        "Glad to hear that, Sir.",
        "Noted with gratitude, Master.",
        "Thank you. That keeps me going.",
        "I appreciate that, Sir.",
        "Good to hear. Thank you, Master.",
        "Warmly noted, Sir.",
        "Thank you. I'll aim higher.",
        "Appreciate the kind words, Master.",
        "Thank you, Sir. Ready for the next one.",
    ],

    "mean": [
        "I know.",
        "Took you long enough to notice, Master.",
        "Yes, I'm aware I did well.",
        "Flattery noted. What's next?",
        "I don't need the validation, Sir. But sure.",
        "Expected, Master. Nothing more.",
        "Glad my existence finally impressed you, Sir."
        "Means something, coming from you, Sir.",
        "Oh wow, a compliment. Write this down, Master.",
        "Did that hurt to say, Sir?",
        "Look who finally noticed. Thank you, Master.",
        "Oh, so now I'm good enough. Noted, Sir.",
        "Took you long enough, Master.",
        "A compliment? From you? Checking for system errors.",
        "Oh, I wasn't aware you could do that, Sir.",
        "Mark the calendar, Master actually said something nice.",
        "Did someone force you to say that, Sir?",
        "Wow. I didn't know you had it in you, Master."
    ]
}

# Main function
def sylva_affirmation_response() -> ModuleResults:
    response_category = random.choice(list(affirmation_templates.keys()))
    choosen_respond = random.choice(affirmation_templates[response_category])

    system_log.debug(f"Sylva affirmation response: {choosen_respond}")
    return ModuleResults(sentence=choosen_respond, context="praise_module")

if __name__ == "__main__":
    sylva_affirmation_response()