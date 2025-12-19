"""Give Sylva access of web searching and provide answer"""

# Importing modules and libraries
from utils import logger, play_voice
from config import ex_config
import serpapi
import random

# Get serpapi API key
serpapi_apikey = ex_config.SERPAPI_APIKEY

# Define utility class
system_log = logger.get_logger(__name__, system=True)
user_log = logger.get_logger(__name__, system=False)

# Sylva phrases templates
sylva_search_templates = [
    "Searching the web for your request, sir.",
    "One moment, sir. I’m scanning the web now.",
    "Understood, sir. Retrieving information from the web.",
    "Allow me to search the web for that, sir.",
    "Checking online sources now, sir.",
    "Initiating web search, sir. Please hold.",
    "Let me look that up on the web for you, sir.",
    "Accessing online data, sir. Just a moment.",
    "Gathering the information you requested from the web.",
    "Running a web search now, sir."
]


def web_search(query: str) -> str:
    serpapi_client = serpapi.Client(api_key=serpapi_apikey)
    try:
        google_search = serpapi_client.search(
            q=query,
            location="Makassar,South Sulawesi,Indonesia",
            engine="google",
        )

    except TimeoutError:
        system_log.error("Google search reach time limit")
        return None
    
    except Exception as e:
        system_log.error(f"Error occured: {e}")
        return None

    if not google_search:
        system_log.debug("Sylva couldn’t find a clear answer")
        return None
    
    try:
        result = google_search["ai_overview"]["text_blocks"][0]["snippet"]
        system_log.debug("Returning ai overview as result")
    except:
        system_log.debug("Couldn't get ai overview")
        result = google_search["organic_results"][0]["snippet"]
        system_log.debug("Give the best match search instead")

    finally:
        return result


def search_result(query: str, tts_agent):
    choosen_template = random.choice(sylva_search_templates)
    voice_path = tts_agent.sylva_voice(choosen_template, "web_search.wav")
    play_voice.play_sound(voice_path)

    result = web_search(query)
    system_log.info("Return search result")
    system_log.info("Proccessing the result")

    result_path = tts_agent.sylva_voice(result, "web_search_result.wav")
    play_voice.play_sound(result_path)

    system_log.debug(f"Search result: {result}")
    user_log.info(f"Search result: {result}")
