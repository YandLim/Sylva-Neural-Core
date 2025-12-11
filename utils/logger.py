"""Logger is an object or a component of a logging system that is used to
record messages and events, providing a trail of information
for debugging, monitoring, and troubleshooting a running software application."""

# Importing modules and libraries
from core import config
import logging
import sys
import os

def get_logger(name: str):
    # Make a log folder to store log file
    log_dir = config.LOG_FOLDER
    os.makedirs(log_dir, exist_ok=True)

    # Create the logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG) # Show all logs (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    
    # Avoid duplicate log 
    if logger.hasHandlers():
        logger.handlers.clear()

    # Custom format for log messages
    formatter = logging.Formatter(
        fmt="[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S" 
    )

    # Show log in the terminal
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # Store log messages into the file
    file_handler = logging.FileHandler(os.path.join(log_dir, "bot_log.log"), encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Execute the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger