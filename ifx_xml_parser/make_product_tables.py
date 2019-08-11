"""
Usage:  make_product_tables.py [--source=FILE_XLSX] [--working_folder=FOLDER]
        [--only=PRODUCT_GROUP] (--working_file=FILE_XLSX...)


Options:
  -h --help
  -s --source=FILE_XLSX                             Input xlsx database
  -r --working_folder=FOLDER                        Working folder [default: .]
  -o --only=PRODUCT_GROUP                           Do only one product group
  -w --working_file=FILE_XLSX...


"""

from docopt import docopt
from excel import read_excel, update_excel_sheet
from mylogger import mylog
import os

from universal_product_table_builder import ProductTableBuilder


def make_product_tables():
    arg = docopt(__doc__)
    mylog.debug(arg)

    in_df, error = read_excel(arg['--source'], replace_nan='')
    if error:
        mylog.error("Can't read file '{0}': {1}".format(arg['--source'], error))
        return

    product_groups = []
    for fn in arg['--working_file']:
        name, ext = fn.split('.', 1)
        if ext == 'xlsx':
            product_groups.append(name)
        else:
            mylog.error("Wrong filename format {0}".format(fn))

    processed_ispn_list = []

    for p_group in product_groups:

        if arg['--only']:
            if p_group != arg['--only']:
                continue

        working_df = in_df.copy()

        mylog.info('Initialization "{0}"'.format(p_group))

        builder = ProductTableBuilder()

        fn = os.path.join(arg['--working_folder'], p_group + ".xlsx")
        sheet_name = 'xml_config'
        mylog.debug("Reading configuration from {0} : {1}".format(fn, sheet_name))
        error = builder.init_from_file(fn, sheet_name=sheet_name)
        if error:
            mylog.error("Can't read configuration from {0} - {1}: {2}".format(fn, sheet_name, error))
            return

        mylog.info('Performing correction steps...')

        builder.do_all_steps(working_df)

        mylog.info("{0} part-numbers processed".format(len(working_df.index)))
        writing_error = update_excel_sheet('Data',
                                           os.path.join(arg['--working_folder'], '{0}.xlsx'.format(p_group)),
                                           working_df,
                                           prompt=True,
                                           convert_strings_to_urls=False)
        if writing_error:
            mylog.error(writing_error)

        processed_ispn_list.extend(working_df['Ispn'].tolist())

    # mark processed Ispns

    mylog.info("Marking processes ispns...")
    in_df['_processed'] = ''
    in_df.loc[in_df['Ispn'].isin(processed_ispn_list), '_processed'] = 'Y'
    mylog.info("Writing back to file {0}...".format(arg['--source']))
    error = update_excel_sheet('', arg['--source'], in_df, prompt=True,
                               convert_strings_to_urls=False)
    if error:
        mylog.error("Can't update {0} with processed Ispns marks".format(arg['--source']))


if __name__ == '__main__':
    make_product_tables()
