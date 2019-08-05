
from anytree import Node


class TreeNode(Node):

    @classmethod
    def new_node(cls, name, parent=None, **kwargs):
        return cls(name, parent, **kwargs)

    def update_data(self, name, obj):
        self.__dict__.update({name: obj})

    def get_data(self, name):
        if name in self.__dict__:
            return self.__dict__[name]
        else:
            return None

    def set_topic(self, topic):
        self.update_data('topic', topic)

    def set_url(self, url):
        self.update_data('url', url)

    def set_flag_new(self, flag: bool):
        self.update_data('flag_new', flag)

    def get_topic(self):
        return self.get_data('topic')

    def get_url(self):
        return self.get_data('url')

    def set_note(self, notes):
        self.update_data('notes', notes)

    def get_note(self):
        return self.get_data('notes')

    def get_flag_new(self):
        return self.get_data('flag_new')


