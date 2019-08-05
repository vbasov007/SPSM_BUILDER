from configparser import RawConfigParser
import io


def get_config(section):
    config_txt = r""" 
                [main]
                input_folder=datafiles
                output_folder=datafiles
                [logging]
                console_level='INFO'
                file_level='DEBUG'
                file='file.log'
                file_format='%(asctime)s %(funcName)s: %(message)s'
                console_format='%(message)s'
                """

    config = RawConfigParser(allow_no_value=True)
    config.read_file(io.StringIO(config_txt))

    items = [(i[0], i[1].strip(' "\'')) for i in config.items(section)]

    return dict(items)
