
CALL bat_config.bat

copy /Y "%IFX_XML_SOURCE_PATH%\%IFX_ISPNS%*.xml" "%IFX_XML_SOURCE_PATH%\ispns.xml"
copy /Y "%IFX_XML_SOURCE_PATH%\%IFX_PRODUCTS%*.xml" "%IFX_XML_SOURCE_PATH%\products.xml"
copy /Y "%IFX_XML_SOURCE_PATH%\%IFX_PARAMETERS%*.xml" "%IFX_XML_SOURCE_PATH%\parameters.xml"
copy /Y "%IFX_XML_SOURCE_PATH%\%IFX_DOCUMENTS%*.xml" "%IFX_XML_SOURCE_PATH%\documents.xml"
copy /Y "%IFX_XML_SOURCE_PATH%\%IFX_DOCUMENTS_ASSIGNMENT%*.xml" "%IFX_XML_SOURCE_PATH%\documents_assignment.xml"
copy /Y "%IFX_XML_SOURCE_PATH%\%IFX_PRODUCT_HIERARCHY%*.xml" "%IFX_XML_SOURCE_PATH%\product_hierarchy.xml"

