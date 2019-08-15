
CALL bat_config.bat

CD "%IFX_XML_PARSER_PATH%"

CALL venv\Scripts\activate

IF "%~1"=="" goto :use_default
	
python make_product_tables.py --source="%IFX_MAKE_TABLES_INPUT_FILE%" --working_folder="%IFX_MAKE_TABLES_WORK_FOLDER%" -w %~1
	
GOTO :finish

:use_default

python make_product_tables.py --source="%IFX_MAKE_TABLES_INPUT_FILE%" --working_folder="%IFX_MAKE_TABLES_WORK_FOLDER%" -m ^
	-w igbt_modules.xlsx ^
	-w mosfets.xlsx ^
	-w igbt_descrete.xlsx ^
	-w ipm_imotion_other_motor_control.xlsx ^
	-w gate_drivers.xlsx


:finish
	
CALL venv\Scripts\deactivate

CD ..