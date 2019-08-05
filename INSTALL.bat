
type README.md

@echo off
set /p var=Continue?[y/n]: 
if not %var%== y goto :EOF

@echo on

CALL bat_config.bat

CD "%IFX_XML_PARSER_PATH%"

virtualenv venv

pip install -r requirements.txt

CD ..

CD "%IFX_HTML_BUILDER_PATH%"

virtualenv venv

pip install -r requirements.txt

CD ..

