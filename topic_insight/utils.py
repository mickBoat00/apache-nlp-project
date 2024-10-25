from urllib.parse import urlparse

def valid_amazon_url(url):
    return urlparse(url).netloc == "www.amazon.com"