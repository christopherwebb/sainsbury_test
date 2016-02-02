import json
import logging
import sys

from SiteCrawler.SiteMapGenerator import SiteMapGenerator

logger = logging.getLogger(__name__)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    begin_url = sys.argv[1]
    result_filename = sys.argv[2]

    generator = SiteMapGenerator(begin_url)

    generator.Process()

    with open(result_filename, 'w') as result_file:
        result_file.write(
            json.dumps({
                'internal': list(generator.internal_pages),
                'static': list(generator.static_content),
                'external': list(generator.external_pages),
                'emails': list(generator.emails)
            }, indent=4, sort_keys=True)
        )
