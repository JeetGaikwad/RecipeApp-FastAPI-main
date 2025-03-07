import logging
import os

logging.getLogger("python_multipart").setLevel(logging.WARNING)
logging.getLogger("passlib").setLevel(logging.WARNING)

logging_levels = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "error": logging.ERROR,
    "warning": logging.WARNING,
    "critical": logging.CRITICAL,
}


# Setup logger function
def setup_logger():
    log_level = (
        logging.DEBUG
        if os.getenv("LOG_LEVEL") == None
        else logging_levels[os.getenv("LOG_LEVEL")]
    )
    logging.basicConfig(level=log_level)
