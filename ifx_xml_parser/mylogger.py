from logging import Logger

from init_mylogger import init_mylogger

mylog: Logger = init_mylogger(FORMAT='$COLOR%(levelname)s $RESET %(relativeCreated)d %(funcName)s: %(message)s')
