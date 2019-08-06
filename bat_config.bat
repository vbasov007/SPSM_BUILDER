
set tool_root=%cd%

SET IFX_ISPNS=IspnsExportJob
SET IFX_PRODUCTS=ProductHierarchyExportJob
SET IFX_PARAMETERS=IspnParametersExportJob
SET IFX_DOCUMENTS=DocumentsExportJob
SET IFX_DOCUMENTS_ASSIGNMENT=DocumentAssignmentsExportJob
SET IFX_PRODUCT_HIERARCHY=ProductHierarchyExportJob

SET IFX_XML_PARSER_PATH=%tool_root%\ifx_xml_parser
SET IFX_XML_SOURCE_PATH=%tool_root%\xml_sources
SET IFX_XML2EXCEL_OUTPUT_PATH=%tool_root%\temp
SET IFX_XML2EXCEL_OUTPUT_FN=%IFX_XML2EXCEL_OUTPUT_PATH%\xml2excel.xlsx
SET IFX_MAKE_TABLES_INPUT_FILE=%IFX_XML2EXCEL_OUTPUT_FN%
SET IFX_MAKE_TABLES_WORK_FOLDER=%tool_root%\data_excel
SET IFX_BUILD_HTML_INPUT_FOLDER=%IFX_MAKE_TABLES_WORK_FOLDER%
SET IFX_BUILD_HTML_OUTPUT_FOLDER=%tool_root%\data_html
SET IFX_HTML_BUILDER_PATH=%tool_root%\product_selection_guide_builder

CD ..
SET SMPS_TOOL_PATH=%cd%\SMPS_TOOL
CD %tool_root%

echo %SMPS_TOOL_PATH%

@echo off
rem setlocal
rem get the date
rem use findstr to strip blank lines from wmic output
for /f "usebackq skip=1 tokens=1-3" %%g in (`wmic Path Win32_LocalTime Get Day^,Month^,Year ^| findstr /r /v "^$"`) do (
  set _day=00%%g
  set _month=00%%h
  set _year=%%i
  )
rem pad day and month with leading zeros
set _month=%_month:~-2%
set _day=%_day:~-2%
rem output format required is DD/MM/YYYY
rem echo %_day%/%_month%/%_year%
rem endlocal

SET DATE_DD_MM_YYYY=%_day%/%_month%/%_year%