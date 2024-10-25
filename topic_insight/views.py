from django.shortcuts import render
from .scraper import AmazonScraper
from .ml_model import OpenAIModel
from .utils import valid_amazon_url

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
            amazon_scraper = AmazonScraper(amazon_product_url)
            customer_reviews_url = amazon_scraper.get_customer_reviews_link()
            customer_reviews = amazon_scraper.generate_customer_reviews(customer_reviews_url)
            if customer_reviews:
                results = OpenAIModel().categorize_reviews(customer_reviews)

        else:
            error_message = "Enter a valid amazon url."

    context = {
        "error_message": error_message,
        "product_page_link": amazon_product_url,
        "customer_reviews_page_link": customer_reviews_url,
        "results": results
    }
    return render(request, 'topic_insight/home.html', context)