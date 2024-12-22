import scrapy
from w3lib.url import url_query_cleaner

from .parse_utils import (
    extract_product_links,
    extract_pagination_links,
    extract_other_links
)

URL_PATTERNS = {
    '//a[contains(@href, "/product/")]/@href',
    '//a[contains(@href, "/products/")]/@href',
    '//a[contains(@href, "/item/")]/@href',
    '//a[contains(@href, "/p/")]/@href'
}

NON_PRODUCT_PATTERNS = {
    '/category/',
}


class BaseEcommerceSpider(scrapy.Spider):
    name = 'base_ecommerce_spider'
    allowed_domains = [
        'scrapingcourse.com',
        'sandbox.oxylabs.io',
        'webscraper.io'
    ]
    start_urls = [
        'https://www.scrapingcourse.com/ecommerce/',
        'https://sandbox.oxylabs.io/products',
        'https://webscraper.io/test-sites/e-commerce/static',
    ]
    visited_urls = set()
    max_depth = 5 # maximum depth to explore the website
    
    def start_requests(self):
        """
        For each start URL, yield a request that includes a meta key 'root_url'
        so we know which branch of the crawl we're following.
        """
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse_listing,
                meta={'root_url': url, 'depth': 0},
            )

    def parse_listing(self, response):
        """
        Default parse method for listing/category pages:
        - Extract & yield product links
        - Follow pagination
        - Explore other links
        """
        root_url = response.meta['root_url']
        depth = response.meta['depth']
        
        # deduplication using cleaned URL but keeping the page parameter
        cleaned_url = url_query_cleaner(response.url, parameterlist=('page'))
        
        if cleaned_url in self.visited_urls or depth > self.max_depth:
            return
        self.visited_urls.add(cleaned_url)

        # Extract & yield product links
        product_links = extract_product_links(
            response, URL_PATTERNS, NON_PRODUCT_PATTERNS
        )
        
        for link in product_links:
            if link not in self.visited_urls:
                self.visited_urls.add(link)
                yield {
                    "product_url": link
                    # yield scrapy.Request(link, callback=self.parse_detail)
                }

        # Pagination links
        pagination_links = extract_pagination_links(response)
        
        for link in pagination_links:
            if link not in self.visited_urls:
                yield scrapy.Request(
                    url=link,
                    callback=self.parse_listing,
                    meta={'root_url': root_url, 'depth': depth},
                )

        # Explore other links (categories, etc.)
        other_links = extract_other_links(response, root_url)
        
        for link in other_links:
            if link not in self.visited_urls:
                yield scrapy.Request(
                    url=link,
                    callback=self.parse_listing,
                    meta={'root_url': root_url, 'depth': depth + 1}
                )
    
    def parse_detail(self, response):
        """
        A placeholder for scraping product detail pages.
        You can override or customize this in a child spider.
        """
        pass
        
