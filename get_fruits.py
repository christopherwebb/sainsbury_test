import json
import logging
import sys

from SiteCrawler.SiteMapGenerator import SiteMapGenerator

logger = logging.getLogger(__name__)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    result_filename = sys.argv[1]

    if len(sys.argv) > 2:
        begin_url = sys.argv[2]
    else:
        begin_url = 'http://hiring-tests.s3-website-eu-west-1.amazonaws.com/2015_Developer_Scrape/5_products.html'

    generator = SiteMapGenerator(begin_url)

    generator.GetProducts()

    with open(result_filename, 'w') as result_file:
        result_file.write(
            json.dumps({
                'results': list(generator.products),
                'total': sum([
                    float(product['unit_price']) for product in generator.products
                ])
            }, indent=4, sort_keys=True)
        )
