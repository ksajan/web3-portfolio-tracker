import logging
import sys

from pythonjsonlogger import jsonlogger


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        if log_record.get("level"):
            log_record["level"] = log_record["level"].upper()
        else:
            log_record["level"] = record.levelname


def get_logger():
    # Create custom logger logging all five levels
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Define format for logs
    fmt = "%(asctime)s  %(level)s  %(message)s"

    # Create stdout handler for logging to the console (logs all five levels)
    stdout_handler = logging.StreamHandler(sys.stdout)

    # Create jsonlogger handler for logging to the console (logs all five levels)
    formatter = CustomJsonFormatter(fmt)
    stdout_handler.setFormatter(formatter)

    # Add both handlers to the logger
    logger.addHandler(stdout_handler)

    return logger


logger = get_logger()
