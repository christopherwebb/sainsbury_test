import unittest

from SiteCrawler.MyHtmlParser import MyHtmlParser
from SiteCrawler.SiteMapGenerator import SiteMapGenerator


class TestParser(unittest.TestCase):
    def test_does_not_add_404_responses(self):
        generator = SiteMapGenerator('http://www.example.com/404')
        generator.parser_class = TestParserClass

        generator.Process()

        self.assertFalse(generator.internal_pages)

    def test_finds_pages(self):
        generator = SiteMapGenerator('http://www.example.com/gets_page')
        generator.parser_class = TestParserClass

        generator.Process()

        self.assertIn('http://www.example.com/gets_page', generator.internal_pages)
        self.assertIn('http://www.example.com/found_page', generator.internal_pages)

    def test_records_redirected_to_pages(self):
        generator = SiteMapGenerator('http://www.example.com/handles_redirects')
        generator.parser_class = TestParserClass

        generator.Process()

        self.assertNotIn('http://www.example.com/handles_redirects', generator.internal_pages)
        self.assertIn('http://www.example.com/actual_page', generator.internal_pages)


# Wrapper class that's injected into the generator to provide test results
class TestParserClass(object):
    def __init__(self, url):
        self.url = url

        emptyResultParser = MyHtmlParser()
        getsPageParser = MyHtmlParser()
        getsPageParser.links = ['http://www.example.com/found_page']

        self.example_results = {
            'http://www.example.com/404': {
                'failure': True,
                'parsed_data': None,
                'url': 'http://www.example.com/404'
            },
            'http://www.example.com/gets_page': {
                'failure': False,
                'parsed_data': getsPageParser,
                'url': 'http://www.example.com/gets_page'
            },
            'http://www.example.com/found_page': {
                'failure': False,
                'parsed_data': emptyResultParser,
                'url': 'http://www.example.com/found_page'
            },
            'http://www.example.com/handles_redirects': {
                'failure': False,
                'parsed_data': emptyResultParser,
                'url': 'http://www.example.com/actual_page'
            },
        }

    def Get(self):
        pass

    def Failure(self):
        return self.example_results[self.url]['failure']

    def GetParsedData(self):
        return self.example_results[self.url]['parsed_data']

    def GetUrl(self):
        return self.example_results[self.url]['url']
