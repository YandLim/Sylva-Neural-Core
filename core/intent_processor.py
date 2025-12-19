"""intent_processor.py takes a user sentence,
sends it to the Rasa model, receives the interpreted intent and entities,
and passes that clean structured data to your main Sylva logic."""

# Importing modules 
from rasa.shared.utils.io import json_to_string
from utils import logger

# Define system log
system_log = logger.get_logger(__name__, system=True)

# Running the model
async def running_model(agent, user_input: str) -> str:
    system_log.info("Starting sylva Neural Core model")

    # Getting result from model
    result = await agent.parse_message(user_input)

    # Getting the required data
    try:
        intentions = result.get("intent", {}).get("name", None)
        try:
            entities = result.get("entities", [])
            value = entities[0]["value"] if entities else None
        except Exception as e:
            system_log.debug(f"{intentions} does not have any value")
    except Exception as e:
        system_log.error(f"Something went wrong with the response: {e}")
        system_log.error(f"{json_to_string(result)}")

    # Return the data
    system_log.debug(f"User input: {user_input}")
    system_log.debug(f"Return the result: Intent={intentions}, Value={value}")
    return intentions, value

