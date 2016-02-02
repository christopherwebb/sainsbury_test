import urllib

from SiteCrawler.MyHtmlParser import MyHtmlParser


class Parser(object):
    def __init__(self, url):
        self.url = url
        self.req_response = None

    def Get(self):
        self.req_response = urllib.urlopen(self.url)

    def Failure(self):
        return self.req_response.getcode() >= 400

    def GetParsedData(self):
        encoding = self.req_response.headers.getparam('charset')
        parsed_data = None
        if encoding:
            parsed_data = self.req_response.read().decode(encoding)
        else:
            parsed_data = self.req_response.read()

        parser = MyHtmlParser()
        parser.feed(parsed_data)

        return parser

    def GetUrl(self):
        return self.req_response.geturl()
