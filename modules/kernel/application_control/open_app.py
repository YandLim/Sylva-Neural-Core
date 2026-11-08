"""Grants Sylva authority to running application installed in the machine."""

# Importing modules 
from utils.dataclasess import ModuleResults
from config import in_config
from utils import logger, function_hint
from pathlib import Path
from utils.play_tts import execute_tts
from . import application_json_setup
import subprocess
import ctypes
import random
import json
import re
import os

# Setup variables
log = logger.get_logger(__name__, system=True)
user_log = logger.get_logger(__name__, system=False)
json_path = Path(in_config.APPLICATION_PATH)

Path(json_path).parent.mkdir(parents=True, exist_ok=True)
if not json_path.exists():
    json_path.write_text("{}") 

# Sylva templates
sylva_template = {
    "success": [
        "{app_name} is now live. All systems report normal operation.",
        "Launch confirmed. {app_name} has entered an active state.",
        "Execution complete. {app_name} is running and responsive.",
        "{app_name} initialized successfully. Standing by for further input.",
        "Startup sequence finished. {app_name} is online.",
        "Command fulfilled. {app_name} has been deployed.",
        "{app_name} is operational. Monitoring stability.",
        "Activation successful. {app_name} is ready for use.",
        "{app_name} launch verified. No anomalies detected.",
        "Process complete. {app_name} is now under your control."
    ],
    "retrying": [
        "I couldn't locate {app}. Attempting a registry sync to find it.",
        "{app} isn't in my index yet. Running a sync before trying again.",
        "No entry for {app}. Scanning the system to update my records.",
        "{app} wasn't found. I'll sync the registry and retry.",
        "That path failed, Sir. Let me sync and locate {app} properly.",
        "{app} is unregistered. Initiating a scan before another attempt.",
        "Couldn't resolve {app}, Master. Syncing the index now.",
        "{app} isn't recognized. Give me a moment to rescan and register it.",
        "Execution failed for {app}. Refreshing my registry first.",
        "{app} is missing from my records. Running a sync to fix that.",
        "No match for {app}, Sir. I'll update the registry and try again.",
        "{app} slipped past my index. Rescanning before retrying.",
        "That didn't work, Master. Syncing my records to find {app}.",
        "{app} isn't logged anywhere I know. Scanning now.",
        "I can't confirm {app} exists yet. Running a registry check.",
        "{app} wasn't where I expected, Sir. Syncing before another pass.",
        "Unregistered target: {app}. Attempting to sync and locate it.",
        "{app} isn't on file, Master. Let me scan and update before retrying.",
        "Failed to launch {app}. Cross-checking with a fresh sync.",
        "{app} came up empty, Sir. Refreshing the registry before I try once more."
    ],
    "failed": [
        "I couldn’t locate {app}. The system reports no valid entry.",
        "{app} is not registered in my application index.",
        "Search completed. {app} was not found on this system.",
        "{app} did not respond. The path appears invalid.",
        "I’m unable to execute {app}. The target is missing.",
        "{app} is unavailable. No launchable source detected.",
        "Request acknowledged, but {app} could not be resolved.",
        "{app} does not exist in the current execution scope.",
        "I checked all known paths. {app} is not accessible.",
        "Execution failed. {app} cannot be found, Master."
    ]
}


# Collecting json_data 
def get_json_data(json_path: Path) -> dict:
    application_data = {}
    try:
        with json_path.open(encoding="utf-8-sig") as f:
            data = json.load(f)
    except:
        with json_path.open(encoding="utf-16") as f:
            data = json.load(f)

    # Cleaning json data 
    for item in data.values():
        application_data[item["Name"].lower()] = {
            "ID": item["ID"],
            "Aliasess": [i.lower() for i in item["Aliasess"]]
        }

    return application_data


# Function to open as admin
def run_as_admin(exe_path: Path) -> None:
    exe_path = os.path.abspath(exe_path)
    cwd = os.path.dirname(exe_path)

    r = ctypes.windll.shell32.ShellExecuteW(
        None,
        "runas",
        exe_path,
        None,
        cwd,
        1
    )

    if r <= 32:
        log.debug(f"ShellExecuteW failed, code={r}")
        raise OSError(f"ShellExecuteW failed, code={r}")

    return


# Main open app function
def open_app(user_input: str) -> True | False:
    found = False
    application_data = get_json_data(json_path)

    # Start checking for every aliases match the user input
    for name, value in application_data.items():
        app_id = value["ID"]

        # If found
        if user_input == name or user_input in value["Aliasess"]:
            log.info(f"App found: {name}, ID: {app_id}")
            found = True

            # Checking the application ID type
            if ".exe" in app_id:  # Type A
                log.info(f"Application {user_input} found as type A")
                try:
                    # If ID contain {6D809377-6AF0-444B-8957-A3773F02200E} type of ID 
                    if "{" in app_id:
                        cleaning = re.sub(r'{[^}]*}', '', app_id)  # Remove the {6D809377-6AF0-444B-8957-A3773F02200E} 
                        paths = [
                            f"C:\\Program Files{cleaning}",
                            f"C:\\Program Files (x86){cleaning}"
                        ]
                        
                        # Looping through 2 program files path
                        for p in paths:
                            try:
                                cwd = os.path.dirname(p)
                                subprocess.Popen([p], cwd=cwd)
                                break
                            except FileNotFoundError:
                                continue
                        else:
                            log.debug(f"App {user_input} are not found in any program files path")
                            raise OSError("App not found")
                    # If not {6D809377-6AF0-444B-8957-A3773F02200E} type, run normally
                    else:
                        subprocess.Popen([app_id], cwd=cwd)

                # Running the application using run as administrator method
                except OSError as e:  # Type A+
                    if getattr(e, "winerror", None) == 740:
                        run_as_admin(p if "{" in app_id else app_id)
                    else:
                        raise

            elif "!" in app_id:  # Type B
                print("Type B")
                subprocess.Popen(["explorer.exe", f"shell:AppsFolder\\{app_id}"])

            else:  # Type C
                print("Type C")
                subprocess.Popen(["cmd", "/c", "start", "", app_id])
            return True

    # If application not found in any aliasess
    if not found:
        log.info(f"Application {user_input} not found")
        print(f"Application {user_input} not found")
        return False


# Sylva run the module
def run_module(application_name: str, tts_agent: function_hint.TTSAgent) -> ModuleResults:
    try:
        openning_app = open_app(application_name)
        
        # If app is found and not found
        if openning_app is True:
            phrase = random.choice(sylva_template["success"])
            sentence = phrase.format(app_name=application_name)
            context = "running_app_success"

        else:
            retry_phrase = random.choice(sylva_template["retrying"])
            retry_sentence = retry_phrase.format(app=application_name)
            context = "retrying_running_app"
            execute_tts(tts_agent, retry_sentence, context)

            application_json_setup.registry_sync()
            openning_app = open_app(application_name)

            if openning_app is True:
                phrase = random.choice(sylva_template["success"])
                sentence = phrase.format(app_name=application_name)
                context = "running_app_success"

            else:
                phrase = random.choice(sylva_template["failed"])
                sentence = phrase.format(app=application_name)
                context = "running_app_failed"
                
        return ModuleResults(sentence=sentence, context=context)
    except Exception as e:
        log.error(f"Something went wrong while trying to open application: {application_name}, {e}")

if __name__ == "__main__":
    run_module(None)