
CALL bat_config.bat

CD "%IFX_XML_PARSER_PATH%"

CALL venv\Scripts\activate

xml2excel.py -f "%IFX_XML_SOURCE_PATH%" -o "%IFX_XML2EXCEL_OUTPUT_FN%"

CALL venv\Scripts\deactivate

CD ..


