
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
		-f igbt_descrete.xlsx ^
		-f ipm_imotion_other_motor_control.xlsx ^
		-f gate_drivers.xlsx ^
		-f switches.xlsx ^
		-f sensors.xlsx ^
		-f lighting_ics.xlsx ^
		-f galium_nitride.xlsx ^
		-f rf_devices.xlsx ^
		-f esd_surge.xlsx ^
		-f power_management_ics.xlsx ^
		-f sic_schottky_diodes.xlsx

		
		
:finish

CALL venv\Scripts\deactivate


CD ..