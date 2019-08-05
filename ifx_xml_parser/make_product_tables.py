"""
Usage:  make_product_tables.py [--source=FILE_XLSX] [--working_folder=FOLDER]
        [--only=PRODUCT_GROUP] [--mark_processed=OUT_FILE] (--config=FILE | --working_file=FILE_XLSX...)


Options:
  -h --help
  -s --source=FILE_XLSX                             Input xlsx database [default: data.xlsx]
  -r --working_folder=FOLDER                        Working folder [default: .]
  -c --config=FILE                                  XLSX config file
  -o --only=PRODUCT_GROUP                           Do only one product group
  -m --mark_processed=OUT_FILE                      Tick off processed Ispns, write back to input file
  -w --working_file=FILE_XLSX...


"""

from docopt import docopt
from excel import read_excel, write_excel, read_sheet_names, add_new_sheet_to_excel
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

    use_config = True

    if arg['--config']:
        product_groups, error = read_sheet_names(arg['--config'])
        if error:
            mylog.error(error)
            return
    elif len(arg['--working_file']) > 0:
        product_groups = []
        use_config = False
        for fn in arg['--working_file']:
            name, ext = fn.split('.', 1)
            if ext == 'xlsx':
                product_groups.append(name)
            else:
                mylog.error("Wrong filename format {0}".format(fn))
    else:
        mylog.error("Config file or working file list have to be defined...")
        return

    rest_ispns_set = set(in_df['Ispn'].tolist())
    ispns_in_total = len(rest_ispns_set)

    processed_ispns = []

    for p_group in product_groups:

        if arg['--only']:
            if p_group != arg['--only']:
                continue

        working_df = in_df.copy()

        mylog.info('Initialization "{0}"'.format(p_group))

        builder = ProductTableBuilder()
        if use_config:
            mylog.debug("Reading configuration from {0} : {1}".format(arg['--config'], p_group))
            error = builder.init_from_file(arg['--config'], sheet_name=p_group)
        else:
            fn = os.path.join(arg['--working_folder'], p_group + ".xlsx")
            sheet_name = 'xml_config'
            mylog.debug("Reading configuration from {0} : {1}".format(fn, sheet_name))
            error = builder.init_from_file(fn, sheet_name=sheet_name)

        if error:
            mylog.error(error)
            return

        mylog.info('Performing correction steps...')

        builder.do_all_steps(working_df)

        rest_ispns_set = rest_ispns_set - set(working_df['Ispn'].tolist())

        mylog.info("{0} part-numbers processed".format(len(working_df.index)))
        writing_error = add_new_sheet_to_excel('Data',
                                               os.path.join(arg['--working_folder'], '{0}.xlsx'.format(p_group)),
                                               working_df,
                                               prompt=True,
                                               convert_strings_to_urls=False,
                                               new_sheet_position='first')
        if writing_error:
            mylog.error(writing_error)

        mylog.info("Processed {0} Ispns out of {1}".format(ispns_in_total - len(rest_ispns_set), ispns_in_total))

        processed_ispns.extend(working_df['Ispn'].tolist())

    if arg['--mark_processed']:
        mylog.info("Ticking off processed Ispns...")

        rest_parts_df = in_df.drop(in_df[in_df['Ispn'].isin(processed_ispns)].index, inplace=False)

        mylog.info('Writing {0}...'.format(arg['--mark_processed']))
        writing_error = write_excel(os.path.join(arg['--working_folder'], arg['--mark_processed']),
                                    rest_parts_df,
                                    prompt=True,
                                    convert_strings_to_urls=False)
        if writing_error:
            mylog.error(writing_error)


if __name__ == '__main__':
    make_product_tables()
