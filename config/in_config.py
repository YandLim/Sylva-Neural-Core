"""All the internal variabels needed for accross the program"""

import os

parent_dir = os.getcwd()
attachment_dir = parent_dir + r"\attachment"

LOG_DIR = attachment_dir + r"\logs"
NOTES_DIR = attachment_dir + r"\user_notes"
REMIND_ME_DIR = attachment_dir + r"\reminders"

APPLICATION_PATH = parent_dir + r"\modules\kernel\application_control\attachment\application_path.json"
USER_WAV = attachment_dir + r"\user_wav.wav"
IOT_DEVICE_PATH =  r"config\iot_device.json"
