from anytree import RenderTree, Node
from argument_parsing_utility import arg_to_header
from dataframe_proc_utility import variations


def print_pretty_tree(root_node, max_nodes=0):

    if max_nodes == 0:
        for pre, fill, node in RenderTree(root_node):
            print("{0}{1}".format(pre, node.name))
    else:
        count = 0
        for pre, fill, node in RenderTree(root_node):
            print("{0}{1}".format(pre, node.name))
            count += 1
            if count > max_nodes:
                print('\n.\n.\n.\n')
                break


def print_pretty_tree_plan(tree_levels, annotation_list=None, notes_list=None, url_col=None):

    print("--------------------TREE PLAN:---------------------")

    root = Node('"{0}"'.format(tree_levels[0]))
    prev_node = root
    for level in tree_levels[1:]:
        new_node = Node('"{0}"'.format(level), parent=prev_node)
        prev_node = new_node

    print_pretty_tree(root)

    if annotation_list:
        print('Annotations: "{0}"'.format(", ".join(annotation_list)))

    if notes_list:
        print('Pop-up notes: "{0}"'.format(", ".join(notes_list)))

    if url_col:
        print('Url link source: "{0}"'.format(url_col))
    print("------------------------END------------------------")


def print_tree(root_node):
    print(RenderTree(root_node))


def print_limited_length(string, max_len=128):
    if len(string) < max_len:
        print(string[:max_len])
    else:
        print(string[:max_len], '...')


def print_header_value_variation_stat(df):

    headers = df.columns.values.tolist()
    i = 1

    for h in headers:
        v = variations(df, h)
        s1 = '{0}. "{1}" - {2}:'.format(i, h, len(v))
        s2 = " "*(40-len(s1)) + ', '.join(v)
        print_limited_length(s1+s2)
        i += 1


def print_all_variations(df, arg, header_dict=None, max_items=999999):

    if header_dict:
        header = arg_to_header(arg, header_dict, df.columns.values.tolist())
    else:
        header = arg

    if header:
        lst = variations(df, header)
        if len(lst) > max_items:
            lst = lst[:max_items]
        print('"{0}": '.format(header))
        print('{0}'.format(repr(", ".join(lst))))
    else:
        print('\n"{0}" not found\n'.format(arg))
