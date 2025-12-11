"""intent_processor.py takes a user sentence,
sends it to the Rasa model, receives the interpreted intent and entities,
and passes that clean structured data to your main Sylva logic."""

# Importing modules 
from rasa.shared.utils.io import json_to_string
from utils import logger

# Define system log
log = logger.get_logger(__name__)

# Running the model
async def running_model(agent, user_input: str) -> str:
    log.info("Starting sylva Neural Core model")

    # Getting result from model
    result = await agent.parse_message(user_input)

    # Getting the required data
    try:
        intentions = result.get("intent", {}).get("name", None)
        try:
            entities = result.get("entities", [])
            value = entities[0]["value"] if entities else None
        except Exception as e:
            log.info(f"{intentions} does not have any value")
    except Exception as e:
        log.info(f"Something went wrong with the response")
        log.error(f"Something went wrong with the response:{e}")
        log.error(f"{json_to_string(result)}")

    # Return the data
    log.info(f"Return the result: Intent={intentions}, Value={value}")
    return intentions, value

