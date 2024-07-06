import logging
import sys
import traceback

from pythonjsonlogger import jsonlogger


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        if log_record.get("level"):
            log_record["level"] = log_record["level"].upper()
        else:
            log_record["level"] = record.levelname

        # Add exception information to the log record
        if record.exc_info:
            log_record["exc_info"] = self.format_exception(record.exc_info)

    def format_exception(self, exc_info):
        """Format exception information as a string."""
        return "".join(traceback.format_exception(*exc_info))


def get_logger(name=__name__, level=logging.INFO):
    # Create custom logger logging all five levels
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Prevent duplicate handlers
    if not logger.hasHandlers():
        # Define format for logs
        fmt = "%(asctime)s  %(level)s  %(message)s"

        # Create stdout handler for logging to the console (logs all five levels)
        stdout_handler = logging.StreamHandler(sys.stdout)

        # Create jsonlogger handler for logging to the console (logs all five levels)
        formatter = CustomJsonFormatter(fmt)
        stdout_handler.setFormatter(formatter)

        # Add the handler to the logger
        logger.addHandler(stdout_handler)

    return logger


logger = get_logger()
