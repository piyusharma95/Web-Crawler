# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
from collections import defaultdict
from urllib.parse import urlparse


class EcommerceCrawlerPipeline:
    def process_item(self, item, spider):
        return item


class DomainToJsonPipeline:
    def __init__(self):
        # domain_map will store { "domain.com": set_of_product_urls }
        self.domain_map = defaultdict(set)

    def process_item(self, item, spider):
        # Each item has a product_url
        product_url = item.get('product_url')
        if product_url:
            domain = urlparse(product_url).netloc
            self.domain_map[domain].add(product_url)
        return item

    def close_spider(self, spider):
        # Convert each set to a list, so it is JSON serializable
        final_data = {domain: list(urls) for domain, urls in self.domain_map.items()}
        
        # Write to a JSON file
        with open('output.json', 'w', encoding='utf-8') as f:
            json.dump(final_data, f, indent=2)


class DomainLinePipeline:
    """
    Writes each product item as a single line of JSON.
    We'll unify them after all spiders finish.
    """
    def open_spider(self, spider):
        self.file = open('output.ndjson', 'a', encoding='utf-8')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        # Each item is written as a single line of JSON
        line = json.dumps(dict(item))
        self.file.write(line + "\n")
        return item