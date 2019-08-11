
CALL bat_config.bat

CD "%IFX_HTML_BUILDER_PATH%"

CALL venv\Scripts\activate

IF "%~1"=="" goto :use_default

python build_tool1.py -i "%IFX_BUILD_HTML_INPUT_FOLDER%" -o "%IFX_BUILD_HTML_OUTPUT_FOLDER%" -d "%DATE_DD_MM_YYYY%" -f %~1

GOTO :finish

:use_default

python build_tool1.py -i "%IFX_BUILD_HTML_INPUT_FOLDER%" -o "%IFX_BUILD_HTML_OUTPUT_FOLDER%" -d "%DATE_DD_MM_YYYY%" ^
		-f igbt_modules.xlsx ^
		-f mosfets.xlsx ^
		-f igbt_descrete.xlsx
		
:finish

CALL venv\Scripts\deactivate


CD ..