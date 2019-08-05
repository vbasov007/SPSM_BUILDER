from anytree import Node
from html_parser import get_div_tag_attributes

from switch_view_html import SwitchableViewHtml


class SwitchableViewMaker:

    def __init__(self):
        self.content_tree_root = Node('root')
        self.level_caption = dict()
        pass

    def _build_content_tree(self, main_category_name, sub_category_name, view_name, table_html):

        def update_tree(node_name, parent):
            for node in parent.children:
                if node.name == node_name:
                    return node
            return Node(node_name, parent=parent)

        def add_data(node, data):
            node.__dict__.update({"table_html": data})

        level = update_tree(main_category_name, self.content_tree_root)
        level = update_tree(sub_category_name, level)
        level = update_tree(view_name, level)
        add_data(level, table_html)

    def add_table(self, table_html):

        attr = get_div_tag_attributes(table_html)

        self._build_content_tree(
            attr['data-main-category'],
            attr['data-subcategory'],
            attr['data-view-name'],
            table_html,)

    def add_level_caption(self, level_num, caption):
        self.level_caption.update({level_num: caption})

    def get_level_caption(self, level_num):
        if level_num in self.level_caption:
            return self.level_caption[level_num]
        else:
            return ''

    def make(self):
        def make_levels(root_node, level_num):
            svh = SwitchableViewHtml()

            if len(root_node.children) > 0:
                for n in root_node.children:
                    svh.add_selectable_content(n.name, n.name, make_levels(n, level_num+1))

                svh.set_title(self.get_level_caption(level_num))
                return svh.make()
            else:
                if "table_html" in root_node.__dict__:
                    return root_node.__dict__['table_html']
                else:
                    return "NO DATA"

        return make_levels(self.content_tree_root, 0)

