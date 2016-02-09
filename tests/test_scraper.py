import unittest

from SiteCrawler.MyHtmlParser import MyHtmlParser
from SiteCrawler.ProductScraper import ProductScraper


class TestParser(unittest.TestCase):
    def test_works_with_404_responses(self):
        generator = ProductScraper('http://www.example.com/404')
        generator.master_parser_class = TestParserClass
        generator.product_parser_class = TestParserClass

        generator.GetProducts()

    def test_finds_pages(self):
        generator = ProductScraper('http://www.example.com/gets_page')
        generator.master_parser_class = TestParserClass
        generator.product_parser_class = TestParserClass

        generator.GetProducts()

        self.assertIn('data', generator.products)

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
                'results': None
            },
            'http://www.example.com/gets_page': {
                'failure': False,
                'results': ['http://www.example.com/found_page']
            },
            'http://www.example.com/found_page': {
                'failure': False,
                'results': 'data'
            },
            'http://www.example.com/handles_redirects': {
                'failure': False,
                'results': emptyResultParser
            },
        }

    def Get(self):
        pass

    def Failure(self):
        return self.example_results[self.url]['failure']

    def GetResults(self):
        return self.example_results[self.url]['results']
