"""Handles question about specific feature."""

# Importing modules and libraries
from utils.dataclasess import ModuleResults
from utils import logger, feature_desc
import random

# Getting class and function
system_log = logger.get_logger(__name__, system=True)
user_log = logger.get_logger(__name__, system=False)

feature_not_found_templates = [
    "I don't have a module by that name, Sir.",
    "That doesn't match anything in my system, Master.",
    "Not in my registry, Sir. Double check the name.",
    "I couldn't find that feature, Master.",
    "Nothing comes up for that, Sir.",
    "That's not a module I recognize, Master.",
    "Doesn't ring a bell, Sir. Try another name.",
    "No match found, Master. That feature may not exist.",
    "I searched. Nothing, Sir.",
    "Can't find that one, Master. Are you sure that's a feature?"
]

# Main function
def exaplain_feature(user_input: str) -> ModuleResults:
    result = False
    choosen_template = random.choice(feature_not_found_templates)
    full_desc_feature = feature_desc.sylva_features

    for feature in full_desc_feature:
        current_dict = full_desc_feature.get(feature)
        aliases = current_dict.get("aliases")
        if user_input == current_dict.get("display") or user_input in aliases:
            result = True
            templates = current_dict.get("description")

    if result is True:
        choosen_template = random.choice(templates)

    system_log.debug(f"Sylva feature introduction: {choosen_template}")
    return ModuleResults(sentence=choosen_template, context="feature_introduction_module")

if __name__ == "__main__":
    exaplain_feature(None)