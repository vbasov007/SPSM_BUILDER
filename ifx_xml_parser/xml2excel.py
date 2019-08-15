"""
Usage: xml2excel.py [--ispn=FILE] [--parameters=FILE] [--docs=FILE] [--docs_assignment=FILE] [--folder=FOLDER] [--output=FILE]

Options:
  -h --help
  -n --ispn=FILE                            IspnsExportJob_YYYY-MM-DD_TIME [default: ispns.xml]
  -p --parameters=FILE                      IspnParametersExportJob_YYYY-MM-DD_TIME  [default: parameters.xml]
  -d --docs=FILE                            DocumentsExportJob_YYYY-MM-DD_TIME  [default: documents.xml]
  -a --docs_assignment=FILE                 DocumentAssignmentsExportJob_YYYY-MM-DD_TIME  [default: documents_assignment.xml]
  -f --folder=FOLDER                        Data folder [default: .]
  -o --output=FILE                          Output file [default: out.xlsx]
"""

from docopt import docopt
from excel import write_excel
import os
from doc_filter import DocFilter
from xml_parsing import xml2excel_params, xml2excel_merge_partnums, \
    ispn_xml_parameters_to_str, document_ref_to_str
from mylogger import mylog
import pandas as pd
from progress import progress


def main():
    arg = docopt(__doc__)

    ispns_fn = arg['--ispn']
    parameters_fn = arg['--parameters']
    docs_fn = arg['--docs']
    docs_assignment_fn = arg['--docs_assignment']
    folder_name = arg['--folder']
    output_fn = arg['--output']

    mylog.info(arg)

    mylog.info('Processing documents...')
    doc_filter = DocFilter()

    file_name = os.path.join(folder_name, docs_fn)
    file_size = os.path.getsize(file_name)
    mylog.info("File size {0} Bytes".format(file_size))
    error = doc_filter.prepare(file_name,
                               progress_indicator=progress,
                               estimated_items_count=int(file_size/1200))
    if error:
        mylog.error(error)
        return
    mylog.info('Processing documents: Done!')

    mylog.info('Processing document assignment...')

    file_name = os.path.join(folder_name, docs_assignment_fn)
    file_size = os.path.getsize(file_name)
    mylog.info("File size {0} Bytes".format(file_size))
    doc_info_df, error = xml2excel_params(file_name,
                                          row_key='Ispn',
                                          column_key='DocumentGroup',
                                          convert2str_method=document_ref_to_str,
                                          is_filter_pass=doc_filter.is_english,
                                          progress_indicator=progress,
                                          estimated_items_count=int(file_size/950))
    if error:
        mylog.error(error)
        return
    mylog.info('Processing document assignment: Done!')

    mylog.info('Processing parameters...')

    file_name = os.path.join(folder_name, parameters_fn)
    file_size = os.path.getsize(file_name)
    mylog.info("File size {0} Bytes".format(file_size))
    ispn_param_df, error = xml2excel_params(file_name,
                                            row_key='Ispn',
                                            column_key='ParameterName',
                                            column_modifier_key='ValueRemark',
                                            convert2str_method=ispn_xml_parameters_to_str,
                                            progress_indicator=progress,
                                            estimated_items_count=int(file_size/870))
    if error:
        mylog.error(error)
        return

    mylog.info('Processing parameters: Done!')

    mylog.info('Processing ispns...')

    file_name = os.path.join(folder_name, ispns_fn)
    file_size = os.path.getsize(file_name)
    mylog.info("File size {0} Bytes".format(file_size))
    ispn_df, error = xml2excel_merge_partnums(file_name,
                                              'Ispn',
                                              progress_indicator=progress,
                                              estimated_items_count=int(file_size/2250))
    if error:
        mylog.error(error)
        return
    mylog.info('Processing ispns: Done!')

    merged_df = pd.merge(ispn_df, ispn_param_df, on='Ispn', suffixes=('_1', '_2'))
    merged_df = pd.merge(merged_df, doc_info_df, on='Ispn', suffixes=('_3', '_4'))

    # merged_df.replace("", "no_data", inplace=True)

    error = write_excel(os.path.join(folder_name, output_fn),
                        merged_df,
                        prompt=True,
                        convert_strings_to_urls=False)
    if error:
        print("Can't write excel file. {0}".format(error))


if __name__ == '__main__':
    main()
