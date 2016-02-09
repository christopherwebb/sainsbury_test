import urllib

from SiteCrawler.MasterPageHtmlParser import MasterPageHtmlParser
from SiteCrawler.ProductPageHtmlParser import ProductPageHtmlParser

from pyquery import PyQuery as pq


class Parser(object):
    def __init__(self, url):
        self.url = url
        self.req_response = None
        self.size = 0

    def Get(self):
        self.req_response = urllib.urlopen(self.url)
        
        encoding = self.req_response.headers.getparam('charset')
        parsed_data = None
        if encoding:
            parsed_data = self.req_response.read().decode(encoding)
        else:
            parsed_data = self.req_response.read()

        self.size = int(self.req_response.info().getheaders('Content-Length')[0])
        self.py_query = pq(parsed_data)

    def Failure(self):
        return self.req_response.getcode() >= 400

    def GetResults(self):
        raise NotImplementedError()


# Scrapes the product index page for product links
class MasterPageParser(Parser):
    def GetResults(self):
        results = self.py_query('ul.productLister .productInfo a')

        return [result.attrib.get("href") for result in results]

# Scrapes the product page for details about the product
class ProductPageParser(Parser):
    def GetResults(self):
        desc_title_results = self.py_query('h3.productDataItemHeader:contains(\'Description\')')
        desc_element = desc_title_results[0].getnext()

        description = ' '.join([child.text for child in desc_element.getchildren() if child.text]).strip()

        pricing_results = self.py_query('.pricing .pricePerUnit')

        title = self.py_query('.productTitleDescriptionContainer h1').text()

        return {
            'description': description,
            'unit_price': float(pricing_results[0].text.strip()[1:]),
            'title': title,
            'size': '%.1fKb' % (self.size / 1024)
        }
