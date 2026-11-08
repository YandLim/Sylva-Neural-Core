"""
light_control.py
Kernel module — direct interface to Tuya-connected lighting hardware.
Handles ON/OFF and scene execution via local key signals..
"""

from utils.dataclasess import ModuleResults
from utils.function_hint import NLUAgent, TTSAgent
from utils.play_tts import execute_tts
from core import intent_processor, stt
from config import in_config, shared_var
from . import device_scan
from typing import Optional
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

# Sylva sentence templates
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

device_not_found_templates = [
    "I don't recognize {device}, Sir. Want me to list what I do see?",
    "No device by that name, Master. Should I show you the registered ones?",
    "{device} isn't on record, Sir. Care to see what's actually registered?",
    "Never heard of it, Master. I can pull up the device list if you want.",
    "That's not registered, Sir. Shall I show you what is?",
    "Come again? {device} doesn't exist in my registry, Master. List, maybe?",
    "Not found, Sir. Either you mistyped it or it's not registered. Want the list?",
    "I've got no record of {device}, Master. I could show you what's actually there.",
    "Unknown device, Sir. Try again, or I can show you the registered ones.",
    "Nothing matches that name, Master. Want a rundown of what's connected?"
]

device_list_templates = [
    "Registered devices, Sir: {device_list}.",
    "Here's what I've got, Master: {device_list}.",
    "Currently registered: {device_list}, Sir.",
    "These are the devices I know, Master: {device_list}.",
    "On record, Sir: {device_list}.",
    "Full list, Master: {device_list}.",
    "Here you go, Sir: {device_list}.",
    "What I can see, Master: {device_list}.",
    "Registry check complete, Sir: {device_list}.",
    "These are your options, Master: {device_list}."
]

device_reconnect_attempt_templates = [
    "{device} isn't responding, Sir. Attempting to reconnect.",
    "Lost connection to {device}, Master. Retrying now.",
    "{device} failed to connect. Give me a moment, Sir.",
    "Connection to {device} dropped, Master. Working on it.",
    "{device} isn't reachable, Sir. Reconnecting automatically.",
    "No response from {device}, Master. I'm retrying now.",
    "{device} went dark, Sir. Attempting to bring it back.",
    "Couldn't reach {device}, Master. Reconnection in progress.",
    "{device} connection failed, Sir. Standby while I retry.",
    "Signal lost to {device}, Master. Reconnecting as we speak."
]

reconnect_success_templates = [
    "Connection restored, Sir. Retrying the command now.",
    "{device} is back online, Master. Trying again.",
    "Got it back, Sir. Reattempting your command.",
    "Reconnected to {device}, Master. Picking up where I left off.",
    "{device} responded this time, Sir. Retrying now.",
    "Connection re-established, Master. Let's try that again.",
    "{device} is reachable again, Sir. Command retrying.",
    "Back online, Master. Executing your original command now.",
    "There it is, Sir. {device} responded. Retrying.",
    "Contact restored, Master. Running the command again.",
    "{device} finally answered, Sir. Trying the command once more.",
    "Reconnection successful, Master. Reattempting now.",
    "Good, {device} is up, Sir. Retrying the command.",
    "Link restored, Master. Command going through again.",
    "{device} is talking again, Sir. Picking up the command.",
    "That worked, Master. Retrying your original request.",
    "Connection confirmed, Sir. Executing again.",
    "{device} came back, Master. Retrying now.",
    "Reconnected, Sir. Second attempt in progress.",
    "Alright, {device} is online again, Master. Trying once more."
]

command_abort_templates = [
    "Command aborted, Sir.",
    "Cancelled, Master. Standing by.",
    "Aborting. Nothing was changed, Sir.",
    "Understood, Master. Command dropped.",
    "Never mind, then, Sir. Aborted.",
    "Command cancelled, Master. No harm done.",
    "Scrapped it, Sir. Say the word if you change your mind.",
    "Aborted, Master. Back to standby.",
    "Command withdrawn, Sir. No action taken.",
    "Fine, Master. Aborting.",
    "Cancelled, Sir. That was quick.",
    "Aborted. Waiting for your next move, Master.",
    "Command terminated before execution, Sir.",
    "As you wish, Master. Aborting.",
    "Dropped it, Sir. Let me know if that changes.",
    "Aborted, Master. Nothing happened, if that helps.",
    "Cancelled. Not that I was attached to it, Sir.",
    "Command halted, Master. No changes made.",
    "Understood, Sir. Standing down.",
    "Aborted, Master. I'll pretend that never happened."
]


# Get device from user value and get the data
def get_device_data(user_target_device: str) -> dict | None:
    system_log.debug(f"Target device: {user_target_device}")

    # Device name containts "_" but user command not
    if user_target_device.replace(" ", "_") in device_list:
        target_device = device_list.get(user_target_device.replace(" ", "_"))

        device_data = {
            "device_id": target_device["device_id"],
            "ip_address": target_device["ip_address"],
            "local_key": target_device["local_key"],
            "version": target_device["version"]
        }

        return device_data

    # Return None if no device found
    return None


# Asking for input and determine the intent
def input_intent(nlu_agent: NLUAgent):
    system_log.info("Running input_intent")

    # Retrying to prevent user_command become None
    for _ in range(max_try):
        if shared_var.vcinput is True:
            user_command = stt.speech_recognition()
            if not user_command:
                continue
        else:
            user_command = input("Master, Your Command: ")

        # If intent error, it return None
        intent, value = asyncio.run(intent_processor.running_model(nlu_agent, user_command))
        if not intent:
            continue # Error = try again

        return intent, value
    return None, None # Error = abort the command


# Main function
def turn_light(user_target_device: str, user_input: str, tts_agent:TTSAgent, nlu_agent: Optional[NLUAgent]= None) -> ModuleResults:
    device_data = get_device_data(user_target_device)

    # No device found
    if not device_data:
        system_log.warning(f"Can't identified device: {user_target_device}")
        not_found_sentences = random.choice(device_not_found_templates).format(device=user_target_device)
        execute_tts(tts_agent, not_found_sentences, "iot_control_module")

        # Offering device list or not
        intent, new_value = input_intent(nlu_agent)

        # Shown device list
        if intent == "affirm":
            all_device = []
            for key, _ in device_list.items():
                all_device.append(key)

                if next(reversed(device_list)) == key and len(device_list) > 1:
                    all_device[-1] = f"And {key}"
            
            full_device_list = ". ".join(f"{i}" for i in all_device)
            device_list_template = random.choice(device_list_templates).format(device_list=full_device_list)
            
            return ModuleResults(sentence=device_list_template, context="iot_control_module")

        # User provide another device name
        elif intent == "iot_control":
            device_data = get_device_data(new_value)

        # Still no device found
        if not device_data:
            return ModuleResults(sentence=random.choice(command_abort_templates), context="iot_control_module")


    # User input won't be in on or off. Unless run from testing.py
    if user_input not in ["on", "off"]:
        # Remove some word for clearer on/off intent detection
        cleaned_user_input = user_input.replace(user_target_device, "").replace("the", "")

        # Running natural language understanding model to determine targeted state
        intent, _ = asyncio.run(intent_processor.running_model(nlu_agent, cleaned_user_input))
        if user_input in ["turn_on", "turn_off"]:
            target_state = intent
        else:
            ask_sentence = random.choice(state_clarify_templates).format(device=user_target_device)
            execute_tts(tts_agent, ask_sentence, "iot_control_module")
            intent, _ = input_intent(nlu_agent)

            if intent in ["turn_on", "turn_off"]:
                target_state = intent
            else:
                return ModuleResults(sentence=random.choice(command_abort_templates), context="iot_control_module")

    system_log.info("Conneting with device")
    d = tinytuya.OutletDevice(device_data["device_id"], device_data["ip_address"], device_data["local_key"])
    d.set_version(device_data["version"])
    d.connection_timeout = 3

    # Get device status
    status = d.status()
    if "Error" in status:
        system_log.error(f"Device return error: {status}")
        result = {
            "device": user_target_device,
            "state": "Error"
        }

        # Running tinytuya scan device
        retrying_template = random.choice(device_reconnect_attempt_templates).format(**result)
        execute_tts(tts_agent, sentence=retrying_template, wav_ctx="iot_control_module")
        scan_result, new_data = device_scan.get_device_data(device_list, user_target_device, device_data["device_id"])

        # If the scan is failed
        if scan_result is False:
            system_log.error("Scanning failed")
            fail_template = random.choice(device_fail_templates)
            fail_sentence = fail_template.format(**result)

            return ModuleResults(sentence=fail_sentence, context="iot_control_module")

        # Scan success and retrying conenction
        system_log.info("Scanning success")
        retry_sentence = random.choice(reconnect_success_templates).format(device=user_target_device)
        execute_tts(tts_agent, sentence=retry_sentence, wav_ctx="iot_control_module")

        d = tinytuya.OutletDevice(new_data["device_id"], new_data["ip_address"], new_data["local_key"])
        d.set_version(new_data["version"])
        status = d.status()

        # Still returning error
        if "Error" in status:
            system_log.error(f"Device return error again: {status}")
            fail_template = random.choice(device_fail_templates)
            fail_sentence = fail_template.format(**result)

            return ModuleResults(sentence=fail_sentence, context="iot_control_module")

    # Turning on/off
    if target_state == "turn_on" or user_input == "on":
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