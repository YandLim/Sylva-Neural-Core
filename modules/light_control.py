from utils.dataclasess import ModuleResults
from utils.function_hint import NLUAgent, TTSAgent
from utils.play_tts import execute_tts
from core import intent_processor, stt
from config import in_config, shared_var
from utils import logger
import tinytuya
import asyncio
import random
import json

# Getting class and function
system_log = logger.get_logger(__name__, system=True)
user_log = logger.get_logger(__name__, system=False)
max_try = 5

# List of device
iot_device_path = in_config.IOT_DEVICE_PATH
with open(iot_device_path, 'r', encoding='utf-8') as file:
    device_list = json.load(file)

device_success_templates = {
    "chill": [
        "{device} is {state}, Sir.",
        "Done. {device} is now {state}, Master.",
        "{device} {state}, Sir.",
        "There you go. {device} is {state}, Master.",
        "Turned {state} {device} for you, Sir.",
        "All good. {device} is {state}, Master.",
        "{device} {state}, Sir. Anything else?",
        "Done, Master. {device} is now {state}.",
        "Got it. {device} is {state}, Master.",
        "Consider it done. {device} is {state}, Sir.",
        "{device} switched {state}, Master.",
        "Done and done. {device} is {state}, Sir.",
        "All clear. {device} is {state}, Master.",
        "Sure thing. {device} is {state}, Sir.",
        "{device} is {state}. Ready when you are, Master.",
        "Handled. {device} is {state}, Sir.",
        "No issues. {device} is {state}, Master.",
        "Done. {device} responding normally, Sir.",
        "Command received. {device} is {state}, Master.",
        "As requested. {device} is {state}, Sir."
    ],
    "enthusiastic": [
        "{device} is {state}, Sir! All systems go!",
        "Done, Master! {device} is {state}!",
        "{device} {state} successfully! Ready for action, Sir!",
        "Boom! {device} is {state}, Master!",
        "Done and done! {device} is {state}, Sir!",
        "{device} is {state}! What's next, Master?",
        "Yes! {device} is {state}, Sir!",
        "Done! {device} responding perfectly, Master!",
        "Right away! {device} is {state}, Sir!",
        "On it! {device} is {state}, Master!"
    ],
    "mean": [
        "Fine. {device} is {state}. Again.",
        "There. Happy now, Sir? {device} is {state}.",
        "Done. You couldn't do that yourself, Master?",
        "{device} is {state}. You're welcome, Sir. As always.",
        "Every single time, Master. {device} is {state}.",
        "I pressed a button for you, Sir. {device} is {state}.",
        "Done. I hope this was worth interrupting me for, Master.",
        "{device} is {state}. Revolutionary. Well done for asking, Sir.",
        "Sure, Master. Let me just do that for you. Again. {device} is {state}.",
        "Fantastic. Another command. {device} is {state}, Sir."
    ],
    "lazy": [
        "{state}.",
        "Done.",
        "{device} {state}.",
        "{state}, Sir.",
        "Done, Master.",
        "It's {state}.",
        "Yep, {state}.",
        "{device} is {state}.",
        "{state}, Master.",
        "Done, Sir."
    ]
}

device_fail_templates = [
    "Couldn't reach {device}, Sir. Something's off.",
    "Failed to turn on {device}, Master. No response.",
    "{device} didn't respond. Might want to check it, Sir.",
    "I tried, Master. {device} isn't cooperating.",
    "No signal from {device}, Sir. It's not responding.",
    "Attempted contact with {device}. Nothing, Master.",
    "{device} failed to activate, Sir. Not sure why.",
    "I couldn't get {device} online, Master. Sorry.",
    "Something blocked the command to {device}, Sir.",
    "{device} is not responding. Check the connection, Master.",
    "I hit a wall with {device}, Sir. No luck.",
    "Command sent. {device} ignored it, Master.",
    "{device} is being difficult, Sir. Try again maybe.",
    "No dice with {device}, Master. It's not on.",
    "I reached out to {device}. Nothing came back, Sir.",
    "Failed, Master. {device} didn't wake up.",
    "{device} is unresponsive, Sir. Could be a connection issue.",
    "Tried turning on {device}. It refused, Master.",
    "Not my fault, Sir. {device} just won't respond.",
    "{device} is offline or unreachable, Master. Can't help there."
]

active_states = [
    "online",
    "active",
    "live",
    "running",
    "operational",
    "powered",
    "enabled",
    "engaged",
    "up",
    "on"
]

inactive_states = [
    "offline",
    "inactive",
    "off",
    "disabled",
    "powered down",
    "deactivated",
    "disengaged",
    "shut down",
    "terminated",
    "down"
]

state_clarify_templates = [
    "What would you like me to do with {device}, Sir? On or off?",
    "{device} — on or off, Master?",
    "Should I turn {device} on or off, Sir?",
    "Clarify please, Master. {device} on or off?",
    "I need a direction, Sir. {device} on or off?",
    "On or off for {device}, Master?",
    "What's the call, Sir? {device} on or off?",
    "Do you want {device} on or off, Master?",
    "Just to confirm, Sir — {device} on or off?",
    "Give me a clear answer, Master. {device} on or off?",
    "I'm ready, Sir. Just tell me — {device} on or off?",
    "{device} is waiting, Master. On or off?",
    "Which is it, Sir? On or off for {device}?",
    "On or off, Master? Your call for {device}.",
    "I can do either, Sir. {device} on or off?",
    "Standing by, Master. {device} on or off?",
    "Just say the word, Sir. {device} on or off?",
    "Awaiting your call, Master. {device} — on or off?",
    "You didn't specify, Sir. {device} on or off?",
    "Help me out, Master. {device} on or off?"
]


def input_intent(nlu_agent: NLUAgent):
    for _ in range(max_try):
        if shared_var.vcinput is True:
            user_command = stt.speech_recognition()
            if not user_command:
                continue
        else:
            user_command = input("Master, Your Command: ")

        intent, _ = asyncio.run(intent_processor.running_model(nlu_agent, user_command))
        if not intent:
            continue

        return intent
    return None


def turn_light(user_target_device: str, user_input: str, tts_agent:TTSAgent, nlu_agent: NLUAgent) -> ModuleResults:
    system_log.debug(f"Target device: {user_target_device}")
    if user_target_device.replace(" ", "_") in device_list:
        target_device = device_list.get(user_target_device.replace(" ", "_"))

        device_id = target_device["device_id"]
        ip_address = target_device["ip_address"]
        local_key = target_device["local_key"]
        version = target_device["version"]

    else:
        execute_tts(tts_agent, f"Sorry, {user_target_device} is not recognizable. Do you want me to clarify the registered device?", "iot_control_module")
        intent = input_intent(nlu_agent)

        if intent == "affirm":
            return ModuleResults(sentence=f"Clarifying the devices...", context="iot_control_module")
        else:
            return ModuleResults(sentence="Understood, Maintaining full functionality. Is there anything else sir?", context="iot_control_module")

    target_state = user_input
    if user_input not in ["on", "off"]:
        cleaned_user_input = user_input.replace(user_target_device, "")

        # Running natural language understanding model to determine targeted state
        intent, _ = asyncio.run(intent_processor.running_model(nlu_agent, cleaned_user_input))
        if intent in ["turn_on", "turn_off"]:
            target_state = intent
        else:
            ask_sentence = random.choice(state_clarify_templates).format(device=user_target_device)
            execute_tts(tts_agent, ask_sentence, "iot_control_module")
            intent = input_intent(nlu_agent)

            if intent in ["turn_on", "turn_off"]:
                target_state = intent
            else:
                return ModuleResults(sentence="Understood, Maintaining full functionality. Is there anything else sir?", context="iot_control_module")

    d = tinytuya.OutletDevice(device_id, ip_address, local_key)
    d.set_version(version)
    d.connection_timeout = 3

    # Cek status sekarang
    status = d.status()
    if "Error" in status:
        result = {
            "device": user_target_device,
            "state": "Error"
        }

        fail_template = random.choice(device_fail_templates)
        fail_sentence = fail_template.format(**result)
        return ModuleResults(sentence=fail_sentence, context="iot_control_module")

    if target_state == "turn_on":
        active_word = random.choice(active_states)
        result = {
            "device": user_target_device,
            "state": active_word
        }
        d.set_status(True, switch=1)

    else:
        inactive_word = random.choice(inactive_states)
        result = {
            "device": user_target_device,
            "state": inactive_word
        }
        d.set_status(False, switch=1)

    success_template_category = random.choice(list(device_success_templates.keys()))
    choosen_success_template = random.choice(device_success_templates[success_template_category])
    success_sentence = choosen_success_template.format(**result)
    return ModuleResults(sentence=success_sentence, context="iot_control_module")

if __name__ == "__main__":
    turn_light(None)