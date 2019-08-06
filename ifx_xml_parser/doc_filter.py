from error import Error
from xml_parsing import xml2dict
# from mylogger import mylog


class DocFilter:

    def __init__(self):
        self.doc_lang = {}

    def prepare(self, doc_info_xml_file: str, *, progress_indicator=None, estimated_items_count=0) -> Error:

        self.doc_lang, error = xml2dict(doc_info_xml_file,
                                        'ObjectName',
                                        'Language',
                                        progress_indicator=progress_indicator,
                                        estimated_items_count=estimated_items_count)
        return error

    def is_english(self, item) -> bool:
        key = item['ObjectName']
        if key in self.doc_lang:
            if self.doc_lang[key] == 'en' or self.doc_lang[key] == 'en,de' or self.doc_lang[key] == 'de,en':
                return True

        return False
