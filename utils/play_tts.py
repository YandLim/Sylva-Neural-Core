""" Execute text to speech function"""

from .function_hint import TTSAgent
from . import logger, play_voice

system_log = logger.get_logger(__name__, system=True)
user_log = logger.get_logger(__name__, system=False)

def execute_tts(tts_agent: TTSAgent, sentence: str, wav_ctx: str) -> None:
    system_log.info("Executing text to speech function")
    wav_path = tts_agent.sylva_voice(sentence, f"{wav_ctx}.wav")
    play_voice.play_sound(wav_path)
    user_log.info(f"Sylva: {sentence}")
    return