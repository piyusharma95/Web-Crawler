import json
import time

from scrapy_selenium import SeleniumRequest
from .base_ecommerce_spider import BaseEcommerceSpider
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.http.response.html import HtmlResponse


class LoadMoreSpider(BaseEcommerceSpider):
    name = 'load_more_spider'
    start_urls = [
        'https://webscraper.io/test-sites/e-commerce/more'
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(
                url=url,
                callback=self.parse_listing,
                meta={'root_url': url, 'depth': 0},
                wait_time=2,  # wait for JS
            )

    def parse_listing(self, response):
        """
        - Use Selenium to click 'Load More' a few times
        - Extract the updated HTML
        - Then pass that HTML to our normal parse logic
        """
        if not response.css('.ecomerce-items-scroll-more'):
            # Reuse the base logic
            yield from super().parse_listing(response)
        else:
            driver = self.driver

            self.remove_cookie_banner(driver)
            
            count = 0
            while True:
                try:
                    # Wait until the "Load More" button is clickable
                    load_more_button = WebDriverWait(driver, 20).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, '.ecomerce-items-scroll-more'))
                    )
                    from selenium.webdriver import ActionChains
                    ActionChains(driver).move_to_element(load_more_button).click().perform()
                    # driver.execute_script("arguments[0].scrollIntoView(true);", load_more_button)
                    time.sleep(2)
                    load_more_button.click()
                    count += 1
                    self.logger.info(f"{response.url} - 'Load More' clicked {count} times")

                except Exception as e:
                    self.logger.info(f"Error clicking 'Load More' button: {e}")
                    break  # Exit the loop if there's no "Load More" button or an error occurs
            
            
            # Extract the updated page source
            updated_response = HtmlResponse(
                driver.current_url,
                body=driver.page_source,
                encoding='utf-8',
                request=response.request
            )
            # Re-extract the products from the updated response
            new_data_items = updated_response.css('div.ecomerce-items-more::attr(data-items)').get()
            if new_data_items:
                new_products = json.loads(new_data_items)
                root_url = response.meta['root_url']
                for product in new_products:
                    link = root_url + '/product/' + str(product.get('id'))
                    if link not in self.visited_urls:
                        self.visited_urls.add(link)
                        yield {
                            "product_url": link
                        }

    def remove_cookie_banner(self, driver):
        try:
            # remove the cookie banner
            driver.execute_script("document.querySelector('#cookieBanner').remove();")
        except Exception as e:
            pass