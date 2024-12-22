import scrapy

url_patterns = {
    '//a[contains(@href, "product")]/@href',
    '//a[contains(@href, "item")]/@href',
    '//a[contains(@href, "/p/")]/@href'
}

class EcommerceSpider(scrapy.Spider):
    name = 'ecommerce_spider'
    allowed_domains = ['scrapingcourse.com']
    start_urls = ['https://www.scrapingcourse.com/ecommerce/']

    def parse(self, response):
        for pattern in url_patterns:
            product_links = response.xpath(pattern).getall()
            for link in product_links:
                yield {"product_url": response.urljoin(link)}

