from w3lib.url import url_query_cleaner


def extract_product_links(response, url_patterns, non_product_patterns):
    """
    Extract potential product links from a response, based on a set of XPath patterns.
    Filter out links containing known 'non_product_patterns'.
    Returns a list of cleaned, full URLs.
    """
    product_urls = set()
    for pattern in url_patterns:
        links = response.xpath(pattern).getall()
        for link in links:
            full_link = url_query_cleaner(response.urljoin(link))
            # Skip if it contains non-product patterns
            if any(pattern in full_link for pattern in non_product_patterns):
                continue
            product_urls.add(full_link)
    return product_urls

def extract_pagination_links(response):
    """
    Example function to extract pagination links (if any).
    This looks for any <a> with 'page' in the URL. Adjust as needed.
    Returns a list of absolute URLs.
    """
    pagination_links = response.xpath('//a[contains(@href, "page")]/@href').getall()
    return {response.urljoin(link) for link in pagination_links}

def extract_other_links(response, root_url):
    """
    Extract generic <a> links from the page, returning those
    that are within the same domain/path (`root_url`).
    """
    all_links = response.xpath('//a/@href').getall()
    valid_links = set()
    for link in all_links:
        full_link = response.urljoin(link)
        if full_link.startswith(root_url):
            valid_links.add(full_link)
    return valid_links
