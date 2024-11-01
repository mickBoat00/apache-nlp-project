import re
from urllib.parse import urlparse

def valid_amazon_url(url):
    return urlparse(url).netloc == "www.amazon.com"

def get_product_asin_from_url(url):
    path = urlparse(url).path
    match = re.search(r'/dp/([A-Z0-9]{10})', path)
    if match:
        return match.group(1)
    return None