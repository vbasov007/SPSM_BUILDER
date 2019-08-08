from argument_parsing_utility import turn_to_list
from product_tree import table_to_tree, parameter_names_tree, table_to_short_table
from argument_parsing_utility import parse_col_equal_to_list_argument
from data_prefilter import include_only_data, exclude_data, include_if_match_string
from tree_node import TreeNode
from html_template import ProductTableOnly
from html_builder import tree_to_html, table_to_html
from argument_parsing_utility import arg_to_header


def filtered_product_table(df, *,
                           exclude,
                           include_only,
                           match,
                           alias_to_col_name_dict=None):
    a_include_only = []
    a_exclude = []

    if len(include_only) > 0:
        a_include_only = include_only.split(';')

    if len(exclude) > 0:
        a_exclude = exclude.split(';')

    a_match = match

    header_dict = alias_to_col_name_dict
    header_list = df.columns.values.tolist()

    for a in a_include_only:
        col, val = parse_col_equal_to_list_argument(a)
        df = include_only_data(df, arg_to_header(col, header_dict, header_list), val)

    for a in a_exclude:
        col, val = parse_col_equal_to_list_argument(a)
        df = exclude_data(df, arg_to_header(col, header_dict, header_list), val)

    if a_match:
        col, val = parse_col_equal_to_list_argument(a_match)
        df = include_if_match_string(df, arg_to_header(col, header_dict, header_list), val[0])

    return df


def product_table_to_html(df, *,
                          category,
                          subcategory,
                          view_name,
                          main_topic,
                          tree_attributes,
                          part_attributes,
                          view_type,
                          datasheet_url,
                          product_page_url,
                          exclude,
                          include_only,
                          match,
                          alias_to_col_name_dict=None):
    a_tree_levels = turn_to_list(tree_attributes.split())
    a_annotations = turn_to_list(part_attributes.split())

    a_main_topic_name = main_topic

    a_include_only = []
    a_exclude = []

    if len(include_only) > 0:
        a_include_only = include_only.split(';')

    if len(exclude) > 0:
        a_exclude = exclude.split(';')

    a_match = match

    print("a_tree_levels:", a_tree_levels)
    print("a_annotations:", a_annotations)
    print("a_main_topic_name:", a_main_topic_name)
    print("a_include_only:", a_include_only)
    print("a_exclude:", a_exclude)
    print("a_match:", a_match)

    df = df.astype(str)

    header_dict = alias_to_col_name_dict

    a_datasheet_url_col = header_dict[str(datasheet_url)]
    a_product_page_url = header_dict[str(product_page_url)]

    header_list = df.columns.values.tolist()

    for a in a_include_only:
        col, val = parse_col_equal_to_list_argument(a)
        df = include_only_data(df, arg_to_header(col, header_dict, header_list), val)

    for a in a_exclude:
        col, val = parse_col_equal_to_list_argument(a)
        df = exclude_data(df, arg_to_header(col, header_dict, header_list), val)

    if a_match:
        col, val = parse_col_equal_to_list_argument(a_match)
        df = include_if_match_string(df, arg_to_header(col, header_dict, header_list), val[0])

    root_node = TreeNode(a_main_topic_name)

    tree_levels = []
    for a in a_tree_levels:
        header = arg_to_header(a, header_dict, header_list)
        if header:
            if not isinstance(header, list):
                header = [header]
        tree_levels.extend(header)

    parameter_names_tree(tree_levels, root_node)

    anns = []
    for a in a_annotations:
        header = arg_to_header(a, header_dict, header_list)
        if header:
            if not isinstance(header, list):
                header = [header]
        anns.extend(header)

    datasheet_url_col = arg_to_header(a_datasheet_url_col, header_dict, header_list)
    product_page_url_col = arg_to_header(a_product_page_url, header_dict, header_list)

    notes = []

    if view_type == 'tree':
        table_to_tree(
            df,
            tree_levels,
            root_node,
            anns,
            notes,
            datasheet_url_col_name=datasheet_url_col,
            product_page_url_col_name=product_page_url_col)

        html_data = tree_to_html(
            root_node,
            ProductTableOnly,
            category=category,
            subcategory=subcategory,
            view_name=view_name)
    elif view_type == 'table':
        short_df = table_to_short_table(df,
                                        col_names_list=tree_levels,
                                        ispn_col_name='Ispn',
                                        datasheet_url_col_name=datasheet_url_col,
                                        product_page_url_col_name=product_page_url_col,
                                        new_product_col_name='new_product')
        html_data = table_to_html(short_df,
                                  ProductTableOnly,
                                  category=category,
                                  subcategory=subcategory,
                                  view_name=view_name)

    return html_data
