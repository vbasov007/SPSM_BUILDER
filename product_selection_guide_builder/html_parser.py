from html.parser import HTMLParser


class DivTagReader(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.category = None
        self.subcategory = None
        self.view = None

        self.attributes = None
        self.tag_found = False

    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            if not self.tag_found:
                self.attributes = attrs
                self.tag_found = True

    def get_attributes(self):
        return self.attributes


def get_div_tag_attributes(html):
    parser = DivTagReader()

    for i in range(0, len(html), 1024):
        parser.feed(html[i:i+1024])
        if parser.tag_found:
            break

    return dict(parser.get_attributes())
