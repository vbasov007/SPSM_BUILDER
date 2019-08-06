from init_mylogger import init_mylogger

mylog = init_mylogger(output_format='$COLOR%(levelname)s $RESET %(relativeCreated)d %(funcName)s: %(message)s',
                      log_file_name=r"logs\html_builder.log")
