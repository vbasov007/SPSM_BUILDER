"""
Usage: build_tool1 [--in_folder=INPUT_FOLDER] [--out_folder=OUTPUT_FOLDER] [--date=DATE] [-p] (--files=FILE...)

Arguments:
    INPUT_FOLDER        Input data folder
    OUTPUT_FOLDER       Output data folder

Options:
    -h --help
    -i --in_folder=INPUT_FOLDER
    -o --out_folder=OUTPUT_FOLDER
    -f --files=FILE                     list of configuration files
    -p --print                          Print more information
    -d --date=DATE                      Update Date

"""

from docopt import docopt
import os
from html_template import CompleteToolTemplate, MainMenuTemplate
from product_table_to_html import product_table_to_html
from printing_utility import print_header_value_variation_stat

from excel import read_excel

from mylogger import mylog


def build_tool1():
    args = docopt(__doc__)
    mylog.debug(args)

    input_folder = ''
    if args['--in_folder']:
        input_folder = args['--in_folder']

    output_folder = ''
    if args['--out_folder']:
        output_folder = args['--out_folder']

    main_menu = MainMenuTemplate()
    output_files_dict = {}

    for input_file_name in args['--files']:

        input_file_full_path = os.path.join(input_folder, input_file_name)

        config_df, error = read_excel(input_file_full_path, replace_nan='', sheet_name='html_config')

        if error:
            mylog.error(error)
            continue

        config_dict = config_df.to_dict('index')

        row_index_list = list(map(int, list(config_dict)))

        mylog.debug(row_index_list)

        for i in row_index_list:
            row = config_dict[i]

            mylog.debug("ROW#{0}".format(i))
            mylog.debug(row)

            output_file_name = row['output_html']
            if output_file_name not in output_files_dict:
                output_files_dict.update({output_file_name: CompleteToolTemplate()})
                main_menu.add_item(row['main_menu_item'], output_file_name)

        for i in row_index_list:

            row = config_dict[i]

            mylog.debug("Open data: {0} - {1}".format(input_file_full_path, 'Data'))

            df, _ = read_excel(input_file_full_path, replace_nan='', sheet_name='Data')

            alias_to_col_name_dict = None
            try:
                mylog.info("Open column alias file: {0} - {1}".format(input_file_full_path, 'column_aliases'))

                col_alias_df, error = read_excel(input_file_full_path, replace_nan='', sheet_name='column_aliases')
                if error:
                    mylog.error(error)
                    return

                alias_to_col_name_dict = aliases_to_dict(col_alias_df, 'alias')
                print(alias_to_col_name_dict)

            except FileNotFoundError as e:
                mylog.error(e)

            if args['--print']:
                mylog.debug(row)
                print_header_value_variation_stat(df)

            table_html = product_table_to_html(
                df,
                category=row['category'],
                subcategory=row['subcategory'],
                view_name=row['view'],
                main_topic=row['main_topic'],
                tree_attributes=row['tree'],
                part_attributes=row['attributes'],
                datasheet_url=row['datasheet_url'],
                view_type=row['view_type'],
                product_page_url=row['product_page_url'],
                exclude=row['exclude'],
                include_only=row['include_only'],
                match=row['match'],
                alias_to_col_name_dict=alias_to_col_name_dict)

            template = output_files_dict[row['output_html']]
            template.add_table(table_html)

    mylog.debug(output_files_dict)

    for file_name in output_files_dict:
        output_files_dict[file_name].add_main_menu_html(main_menu.make(selected_menu_link=file_name))
        output_files_dict[file_name].add_date_info(args['--date'])
        out_html = output_files_dict[file_name].make()
        with open(os.path.join(output_folder, file_name), "w", encoding='utf-8') as out_html_file:
            out_html_file.write(out_html)


def aliases_to_dict(alias_df, alias_col: str) -> dict:
    al_df = alias_df.set_index(alias_col)
    res = {}
    for index, row in al_df.iterrows():
        row = [r for r in row if len(r) > 0]
        if len(row) == 1:
            row = row[0]
        if len(row) == 0:
            row = ''
        res.update({index: row})

    return res


def build_tool1_test():
    file_list = ["f1.html", "f2.html", "f3.html"]

    template = CompleteToolTemplate()

    for file_name in file_list:
        with open(file_name, "r", encoding='utf-8') as html_file:
            html = html_file.read()
        template.add_table(html)

    out_html = template.make()

    with open("out.html", "w", encoding='utf-8') as out_html_file:
        out_html_file.write(out_html)


if __name__ == '__main__':
    build_tool1()
