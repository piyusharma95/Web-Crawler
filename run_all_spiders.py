import json
from collections import defaultdict
from urllib.parse import urlparse

from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings


def unify_ndjson(ndjson_file, output_file):
    """
    Read line-delimited JSON (NDJSON) from ndjson_file,
    aggregate items by domain, and write a single JSON object
    to output_file.
    """
    domain_map = defaultdict(set)

    with open(ndjson_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            data = json.loads(line)
            # Example: we assume items have "product_url"
            product_url = data.get('product_url')
            if product_url:
                domain = urlparse(product_url).netloc
                domain_map[domain].add(product_url)

    # Convert sets to lists so they're JSON-serializable
    final_data = {d: list(urls) for d, urls in domain_map.items()}

    with open(output_file, 'w', encoding='utf-8') as out:
        json.dump(final_data, out, indent=2)

def main():
    """
    1) Spin up the CrawlerRunner with project settings.
    2) Schedule multiple spiders to run in parallel.
    3) Once done, unify NDJSON lines into a single JSON file.
    4) Stop the reactor.
    """
    settings = get_project_settings()
    runner = CrawlerRunner(settings)

    # Schedule your spiders by name (the 'name' attribute in each spider):
    runner.crawl('base_ecommerce_spider')
    runner.crawl('load_more_spider')
    runner.crawl('ajax_ecommerce_spider')

    # Once all spiders finish, unify NDJSON -> JSON, then stop the reactor
    deferred = runner.join()
    deferred.addCallback(lambda _: unify_ndjson('output.ndjson', 'combined_output.json'))
    deferred.addCallback(lambda _: reactor.stop())

    reactor.run()

if __name__ == "__main__":
    main()
