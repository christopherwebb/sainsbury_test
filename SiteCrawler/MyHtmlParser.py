from HTMLParser import HTMLParser


class MyHtmlParser(HTMLParser):
    def __init__(self, *args, **kwargs):
        # HTMLParser is an old style class
        HTMLParser.__init__(self)
        
        self.links = []
        self.images = []
        self.css = []
        self.scripts = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attr in attrs:
                if attr[0] == 'href':
                    self.links.append(attr[1])

        elif tag == 'img':
            for attr in attrs:
                if attr[0] == 'src':
                    self.images.append(attr[1])

        elif tag == 'link':
            is_stylesheet = False
            src = ''
            for attr in attrs:
                if attr[0] == 'rel':
                    is_stylesheet = 'stylesheet' in attr[1]
                elif attr[0] == 'href':
                    src = attr[1]

            if src and is_stylesheet:
                self.css.append(src)
            elif src:
                self.links.append(src)

        elif tag == 'script':
            for attr in attrs:
                if attr[0] == 'src':
                    self.scripts.append(attr[1])
