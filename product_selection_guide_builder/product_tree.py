import pandas as pd
from validators import url as is_url
from dataframe_proc_utility import variations, take_only, annotations_with_title, get_single_col_value, count_rows
from html_format_utility import span_format, format_multiline_annot, format_val_with_measure_units_html


def table_to_tree(
        df, tree_level_names, parent_node,
        last_level_annotations,
        pop_up_notes,
        datasheet_url_col_name=None,
        product_page_url_col_name=None
):
    if df.empty:
        return

    conditions = variations(df, tree_level_names[0])
    for c in conditions:
        if pd.isna(c):
            continue

        filtered_df = take_only(df, tree_level_names[0], c)

        flag_new_product = False
        if count_rows(filtered_df, 'new_product', 'new'):
            flag_new_product = True

        c = format_val_with_measure_units_html(c)
        c = span_format(tree_level_names[0], c)

        if len(tree_level_names) > 1:
            new_node = parent_node.new_node(c, parent_node)
            new_node.set_flag_new(flag_new_product)

            table_to_tree(
                filtered_df,
                tree_level_names[1:],
                new_node,
                last_level_annotations,
                pop_up_notes,
                datasheet_url_col_name=datasheet_url_col_name,
                product_page_url_col_name=product_page_url_col_name)
        else:
            ann_list = annotations_with_title(filtered_df, last_level_annotations)
            pop_up_notes_list = annotations_with_title(filtered_df, pop_up_notes)

            ann_list.extend(pop_up_notes_list)

            datasheet_url = ''
            if datasheet_url_col_name:
                datasheet_url = get_single_col_value(filtered_df, datasheet_url_col_name)

            product_page_url = ''
            if product_page_url_col_name:
                product_page_url = get_single_col_value(filtered_df, product_page_url_col_name)

            new_node_content = formatted_product_link(c, product_page_url,
                                                      datasheet_url) + '</br>' + format_multiline_annot(ann_list)

            new_node = parent_node.new_node(new_node_content, parent_node)

            new_node.set_flag_new(flag_new_product)

    return


def parameter_names_tree(tree_level_names, attach_to_node):
    prev_node = attach_to_node
    for level in tree_level_names:
        new_node = attach_to_node.new_node('{0}'.format(level), parent=prev_node)
        prev_node = new_node


def table_to_short_table(df, *,
                         col_names_list,
                         ispn_col_name,
                         datasheet_url_col_name,
                         product_page_url_col_name,
                         new_product_col_name):
    out_df = df.copy()

    for index, row in out_df.iterrows():
        new_flag_html = ''
        if out_df.at[index, new_product_col_name]:
            new_flag_html = '<span class="new-prod-flag">NEW</span>'
        out_df.at[index, ispn_col_name] = formatted_product_link(out_df.at[index, ispn_col_name],
                                                                 out_df.at[index, product_page_url_col_name],
                                                                 out_df.at[
                                                                     index, datasheet_url_col_name]) + new_flag_html

    out_df = out_df[col_names_list]

    # format with span tags
    for col_name, col_values in out_df.iteritems():
        if col_name != ispn_col_name:  # don't touch column with Ispns, since it is already formatted
            for index, value in col_values.items():
                value = format_val_with_measure_units_html(value)
                value = span_format(col_name, value)
                out_df.at[index, col_name] = value


    return out_df


def formatted_product_link(product_name, page_url, datasheet_url):
    if is_url(page_url):
        page_url_html = "<a class=product href='{0}' target='_blank'>{1}</a>".format(page_url, product_name)
    else:
        page_url_html = "<span class=product>{0}</span>".format(product_name)

    if is_url(datasheet_url):
        ds_url_html = "<a class=ds_link href='{0}' target='_blank'>datasheet</a>".format(datasheet_url)
    else:
        ds_url_html = ""

    return page_url_html + ds_url_html
