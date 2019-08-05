
CALL bat_config.bat

CD "%IFX_HTML_BUILDER_PATH%"

CALL venv\Scripts\activate

build_tool1.py -i "%IFX_BUILD_HTML_INPUT_FOLDER%" -o "%IFX_BUILD_HTML_OUTPUT_FOLDER%" -f mosfets.xlsx
rem	-f igbt_modules.xlsx ^
rem	-f mosfets.xlsx ^
rem	-f igbt_descrete.xlsx


CALL venv\Scripts\deactivate

CD ..