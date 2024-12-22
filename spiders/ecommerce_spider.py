import scrapy
from w3lib.url import url_query_cleaner

url_patterns = {
    '//a[contains(@href, "/product/")]/@href',
    '//a[contains(@href, "/products/")]/@href',
    '//a[contains(@href, "/item/")]/@href',
    '//a[contains(@href, "/p/")]/@href'
}

non_product_patterns = {
    '/category/',
}


class EcommerceSpider(scrapy.Spider):
    name = 'ecommerce_spider'
    allowed_domains = [
        'www.scrapingcourse.com',
        'sandbox.oxylabs.io'
    ]
    start_urls = [
        'https://www.scrapingcourse.com/ecommerce/',
        'https://sandbox.oxylabs.io/products'
    ]
    visited_urls = set()

    def parse(self, response):
        # deduplication using cleaned URL but keeping the page parameter
        cleaned_url = url_query_cleaner(response.url, parameterlist=('page'))
        if cleaned_url in self.visited_urls:
            return
        self.visited_urls.add(response.url)

        for pattern in url_patterns:
            product_links = response.xpath(pattern).getall()
            for link in product_links:
                full_link = url_query_cleaner(response.urljoin(link))
                
                check_non_product = any([pattern in full_link for pattern in non_product_patterns])
                if check_non_product:
                    continue
                
                if full_link not in self.visited_urls:
                    yield {"product_url": full_link}
                    self.visited_urls.add(full_link)
        
        pagination_links = response.xpath('//a[contains(@href, "page")]/@href').getall()
        for link in pagination_links:
            full_link = response.urljoin(link)
            if full_link not in self.visited_urls:
                yield scrapy.Request(url=full_link, callback=self.parse)
        
