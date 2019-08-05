import logging
from color_logging import ColorFormatter


def init_mylogger(*, LEVEL='DEBUG', FILE='logs\par.log', FORMAT='%(levelname)s %(asctime)s %(funcName)s: %(message)s' ):

    my_logger_name = FILE

    my_logger = logging.getLogger(my_logger_name)

    if not my_logger.hasHandlers():

        level = LEVEL

        my_logger.setLevel(level)

        logger_file_handler = logging.FileHandler(FILE)

        logger_file_handler.setLevel(level)

        logger_console_handler = logging.StreamHandler()
        logger_console_handler.setLevel(level)

        # logger_formatter = logging.Formatter(FORMAT)
        logger_formatter = ColorFormatter(FORMAT)
        # logging.ColorFormatter = ColorFormatter

        logger_console_handler.setFormatter(logger_formatter)
        logger_file_handler.setFormatter(logger_formatter)

        my_logger.addHandler(logger_console_handler)
        my_logger.addHandler(logger_file_handler)

    return my_logger
