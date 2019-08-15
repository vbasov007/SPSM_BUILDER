from argument_parsing_utility import turn_to_list
from product_tree import table_to_tree, parameter_names_tree, table_to_short_table
from argument_parsing_utility import parse_col_equal_to_list_argument
from data_prefilter import include_only_data, exclude_data, include_if_match_string
from tree_node import TreeNode
from html_template import ProductTableOnly
from html_builder import tree_to_html, table_to_html
from argument_parsing_utility import arg_to_header
from error import Error


def selected_products(df, *,
                      exclude,
                      include_only,
                      match,
                      alias_to_col_name_dict=None):
    a_include_only = []
    a_exclude = []
    a_match = []

    if len(include_only) > 0:
        a_include_only = include_only.split(';')

    if len(exclude) > 0:
        a_exclude = exclude.split(';')

    if len(match) > 0:
        a_match = match.split(';')

    header_dict = alias_to_col_name_dict
    header_list = df.columns.values.tolist()

    for a in a_include_only:
        col, val = parse_col_equal_to_list_argument(a)
        df = include_only_data(df, arg_to_header(col, header_dict, header_list), val)

    for a in a_exclude:
        col, val = parse_col_equal_to_list_argument(a)
        df = exclude_data(df, arg_to_header(col, header_dict, header_list), val)

    for a in a_match:
        col, val = parse_col_equal_to_list_argument(a)
        df = include_if_match_string(df, arg_to_header(col, header_dict, header_list), val)

    return df


def column_names_by_alias(alias, alias_to_col_name_dict, colname_list) -> (list, Error):
    header = arg_to_header(alias, alias_to_col_name_dict, colname_list)
    if header:
        if not isinstance(header, list):
            header = [header]
        headers_not_in_columns = list(set(header) - set(colname_list))
        if len(headers_not_in_columns) == 0:
            return header, Error(None)
        else:
            return [], Error("'{0}' are not existing column name".format(headers_not_in_columns))
    else:
        # alias doesn't exist
        return [], Error('Alias "{0}" not defined'.format(alias))


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
                          alias_to_col_name_dict=None) -> (str, Error):
    a_tree_levels = turn_to_list(tree_attributes.split())
    a_annotations = turn_to_list(part_attributes.split())

    a_main_topic_name = main_topic

    df = df.astype(str)

    colname_list = df.columns.values.tolist()

    root_node = TreeNode(a_main_topic_name)

    tree_levels = []
    for a in a_tree_levels:
        headers, err = column_names_by_alias(a, alias_to_col_name_dict, colname_list)
        if err:
            return '', err
        else:
            tree_levels.extend(headers)

    parameter_names_tree(tree_levels, root_node)

    anns = []
    for a in a_annotations:
        headers, err = column_names_by_alias(a, alias_to_col_name_dict, colname_list)
        if err:
            return '', err
        else:
            anns.extend(headers)

    headers, err = column_names_by_alias(datasheet_url, alias_to_col_name_dict, colname_list)
    if err:
        return '', err
    else:
        datasheet_url_col = headers[0]

    headers, err = column_names_by_alias(product_page_url, alias_to_col_name_dict, colname_list)
    if err:
        return '', err
    else:
        product_page_url_col = headers[0]

    notes = []

    if view_type == 'tree':
        error = table_to_tree(df,
                              tree_levels,
                              root_node,
                              anns,
                              notes,
                              datasheet_url_col_name=datasheet_url_col,
                              product_page_url_col_name=product_page_url_col)
        if error:
            return '', error

        html_data = tree_to_html(
            root_node,
            ProductTableOnly,
            category=category,
            subcategory=subcategory,
            view_name=view_name)
    elif view_type == 'table':
        short_df, error = table_to_short_table(df,
                                               col_names_list=tree_levels,
                                               ispn_col_name='Ispn',
                                               datasheet_url_col_name=datasheet_url_col,
                                               product_page_url_col_name=product_page_url_col,
                                               new_product_col_name='new_product')
        if error:
            return '', error

        html_data = table_to_html(short_df,
                                  ProductTableOnly,
                                  category=category,
                                  subcategory=subcategory,
                                  view_name=view_name)
    else:
        return '', Error("Not defined view type")

    return html_data, Error(None)
