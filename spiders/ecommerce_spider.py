import scrapy

url_patterns = {
    '//a[contains(@href, "product")]/@href',
    '//a[contains(@href, "item")]/@href',
    '//a[contains(@href, "/p/")]/@href'
}

class EcommerceSpider(scrapy.Spider):
    name = 'ecommerce_spider'
    allowed_domains = ['www.scrapingcourse.com']
    start_urls = ['https://www.scrapingcourse.com/ecommerce/']
    visited_urls = set()

    def parse(self, response):
        if response.url in self.visited_urls:
            return
        self.visited_urls.add(response.url)
        
        for pattern in url_patterns:
            product_links = response.xpath(pattern).getall()
            for link in product_links:
                full_link = response.urljoin(link)
                if full_link not in self.visited_urls:
                    yield {"product_url": full_link}
                    self.visited_urls.add(full_link)
        
        pagination_links = response.xpath('//a[contains(@href, "/page/")]/@href').getall()
        for link in pagination_links:
            full_link = response.urljoin(link)
            if full_link not in self.visited_urls:
                yield scrapy.Request(url=full_link, callback=self.parse)
        
