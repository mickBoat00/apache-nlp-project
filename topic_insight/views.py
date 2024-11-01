from django.shortcuts import render
from .scraper import AmazonScraper
from .ml_model import OpenAIModel
from .utils import valid_amazon_url, get_product_asin_from_url
from .scraper import OxylabScraperAPI
import json

# Create your views here.
def home(request): 
    error_message = ''
    amazon_product_url = ''
    customer_reviews_url = ''
    results = []
    
    if request.POST:
        product_url = request.POST.get('product_url')

        if valid_amazon_url(product_url):
            amazon_product_url = product_url
            asin = get_product_asin_from_url(product_url)
            scraper = OxylabScraperAPI(asin)
            reviews = scraper.list_reviews()
            results = OpenAIModel(reviews).categorize_reviews()
        else:
            error_message = "Enter a valid amazon url."

    context = {
        "error_message": error_message,
        "product_page_link": amazon_product_url,
        "customer_reviews_page_link": customer_reviews_url,
        "results": results
    }
    return render(request, 'topic_insight/home.html', context)