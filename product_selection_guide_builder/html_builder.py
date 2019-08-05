from tree_node import TreeNode


def tree_to_html_list(root_node: TreeNode):
    child_html = ""
    for node in root_node.children:
        child_html += tree_to_html_list(node)

    href = root_node.get_url()

    new_product_mark_html = ''
    if root_node.get_flag_new():
        new_product_mark_html = '<span class="new-prod-flag">NEW</span>'

    if not href:
        href = '#'

    if len(child_html) > 0:
        return '<li><div class="branch">{0}{2}</div><ul>{1}</ul></li>'.format(
            root_node.name, child_html, new_product_mark_html)
    else:
        return '<li><div class="branch">{1}{0}</div></li>'.format(
            root_node.name, new_product_mark_html)


def tree_to_html(root_node: TreeNode, template, category='', subcategory='', view_name=''):
    page_title = root_node.name

    table_headers_html = ""
    table_content = ""
    for node in root_node.children:
        table_headers_html += '<th>{0}</th>'.format(node.name)
        h = ""
        for sub_node in node.children:
            h += tree_to_html_list(sub_node)

        table_content += '<td class="nowrap"><ul class="tree">{0}</ul></td>'.format(h)

    table_headers_html = "<tr>{0}</tr>".format(table_headers_html)
    table_content = "<tr>{0}</tr>".format(table_content)

    # CHANGED make HERE
    return template().make(
        Category=category,
        Subcategory=subcategory,
        View_Name=view_name,
        Page_Title=page_title,
        Table_Title=page_title,
        Table_Headers=table_headers_html,
        Table_Content=table_content,
    )


def table_to_html(table_df, template, category='', subcategory='', view_name=''):
    table_headers_html = "<th></th>"  # skip first column
    for header in table_df.columns.values:
        table_headers_html += "<th>{0}</th>".format(header)

    table_headers_html = "<tr>{0}</tr>".format(table_headers_html)

    table_content_html = ""
    for row_number, row in table_df.iterrows():
        row_html = "<td></td>"  # skip first column
        for item in row:
            row_html += "<td>{0}</td>".format(item)
        row_html = "<tr>{0}</tr>".format(row_html)
        table_content_html += row_html

    return template().make(
        Category=category,
        Subcategory=subcategory,
        View_Name=view_name,
        Page_Title="page_title",
        Table_Title="page_title",
        Table_Headers=table_headers_html,
        Table_Content=table_content_html)
