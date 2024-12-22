import json

from .base_ecommerce_spider import BaseEcommerceSpider


class AjaxEcommerceSpider(BaseEcommerceSpider):
    """
    Spider specialized for handling AJAX-based e-commerce pages.
    Inherits all the base logic from BaseEcommerceSpider and overrides 
    where necessary.
    """

    name = 'ajax_ecommerce_spider'
    start_urls = [
        'https://webscraper.io/test-sites/e-commerce/ajax'
    ]

    def parse_listing(self, response):
        # Reuse the base logic
        yield from super().parse_listing(response)

        # 2. Then parse the inline JSON data, if present
        data_items = response.xpath(
            '//div[contains(@class, "ecomerce-items-ajax")]/@data-items'
        ).get()

        if data_items:
            # data_items is a string containing JSON, e.g. 
            # '[{"id":1,"title":"Nokia 123","description":"7 day battery","price":24.99}, ...]'
            products = json.loads(data_items)
            root_url = response.meta['root_url']

            # 3. Yield each product as an item or dict
            for product in products:
                link = root_url + '/product/' + str(product.get('id'))
                if link not in self.visited_urls:
                    self.visited_urls.add(link)
                    yield {
                        "product_url": link
                    }
