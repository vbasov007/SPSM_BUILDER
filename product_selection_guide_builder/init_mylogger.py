import logging
from color_logging import ColorFormatter


def init_mylogger(*, logging_level='DEBUG', log_file_name=r"default.log",
                  output_format='%(levelname)s %(asctime)s %(funcName)s: %(message)s'):
    my_logger_name = log_file_name

    my_logger = logging.getLogger(my_logger_name)

    if not my_logger.hasHandlers():
        level = logging_level

        my_logger.setLevel(level)

        logger_file_handler = logging.FileHandler(log_file_name)

        logger_file_handler.setLevel(level)

        logger_console_handler = logging.StreamHandler()
        logger_console_handler.setLevel(level)

        logger_formatter = ColorFormatter(output_format)

        logger_console_handler.setFormatter(logger_formatter)
        logger_file_handler.setFormatter(logger_formatter)

        my_logger.addHandler(logger_console_handler)
        my_logger.addHandler(logger_file_handler)

    return my_logger