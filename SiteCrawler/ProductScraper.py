import logging
import urlparse

from Parser import MasterPageParser, ProductPageParser

logger = logging.getLogger(__name__)


class ProductScraper(object):
    def __init__(self, begin_url):
        self.begin_url = begin_url

        self.master_parser_class = MasterPageParser
        self.product_parser_class = ProductPageParser

        self.products = []

    def GetProducts(self):
        parser = self.master_parser_class(self.begin_url)
        parser.Get()
        if parser.Failure():
            return

        logger.info('parsed: %s' % self.begin_url)
        results = parser.GetResults()

        for product_url in results:
            logger.info('parsed: %s' % product_url)

            product_parser = self.product_parser_class(product_url)

            product_parser.Get()

            if product_parser.Failure():
                continue

            self.products.append(product_parser.GetResults())
