"""Handles question about feature but in general from question like: 'What can you do?'."""

# Importing modules and libraries
from utils.dataclasess import ModuleResults
from utils import logger, feature_desc
import random

# Getting class and function
system_log = logger.get_logger(__name__, system=True)
user_log = logger.get_logger(__name__, system=False)

# Sylva phrases tamplates
feature_list_templates = [
    "Here's what I can do, Sir:\n{features}",
    "My current capabilities, Master:\n{features}",
    "Allow me to run you through my modules, Sir:\n{features}",
    "Here's the full list, Master:\n{features}",
    "What I'm capable of, Sir:\n{features}",
    "Current modules online, Master:\n{features}",
    "My function list, Sir:\n{features}",
    "Here's what I have available, Master:\n{features}",
    "Systems report the following capabilities, Sir:\n{features}",
    "Running you through my active modules, Master:\n{features}",
]

def feature_list() -> ModuleResults:
    features = []
    full_desc_feature = feature_desc.sylva_features
    for key, _ in full_desc_feature.items():
        features.append(key)
        if next(reversed(full_desc_feature)) == key:
            features[-1] = f"And {key}"
    
    full_feature_list = ". ".join(f"{i} module" for i in features)
    choosen_respond = random.choice(feature_list_templates)
    sentence = choosen_respond.format(features=full_feature_list)

    system_log.debug(f"Sylva feature: {sentence}")
    return ModuleResults(sentence=sentence, context="feature_list_module")

if __name__ == "__main__":
    feature_list()

