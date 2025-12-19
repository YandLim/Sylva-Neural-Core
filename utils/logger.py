"""Logger is an object or a component of a logging system that is used to
record messages and events, providing a trail of information
for debugging, monitoring, and troubleshooting a running software application."""

# Importing modules and libraries
from config import in_config
import logging
import sys
import os

def get_logger(name: str, system: True|False=True):
    # Make a log folder to store log file
    log_dir = in_config.LOG_DIR
    if system is True:
        log_type = "system"
        log_file = log_dir + r"\system_log.log"
    else:
        log_type = "user"
        log_file = log_dir + r"\user_log.log"
    os.makedirs(log_dir, exist_ok=True)

    # Create the logger
    logger = logging.getLogger(f"{log_type}.{name}")
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
    file_handler = logging.FileHandler(filename=log_file, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Execute the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
