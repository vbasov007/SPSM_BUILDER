import logging
from configurator import get_config


def init_mylogger():

    my_logger_name = get_config('logging')['file']

    my_logger = logging.getLogger(my_logger_name)

    if not my_logger.hasHandlers():

        file_level = get_config('logging')['file_level']
        console_level = get_config('logging')['console_level']

        my_logger.setLevel(file_level)

        logger_file_handler = logging.FileHandler(get_config('logging')['file'])

        logger_file_handler.setLevel(file_level)

        logger_console_handler = logging.StreamHandler()
        logger_console_handler.setLevel(console_level)

        console_logger_formatter = logging.Formatter(get_config('logging')['console_format'])
        file_logger_formatter = logging.Formatter(get_config('logging')['file_format'])

        logger_console_handler.setFormatter(console_logger_formatter)
        logger_file_handler.setFormatter(file_logger_formatter)

        my_logger.addHandler(logger_console_handler)
        my_logger.addHandler(logger_file_handler)

    return my_logger
