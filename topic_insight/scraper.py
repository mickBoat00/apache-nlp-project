import requests
from bs4 import BeautifulSoup
from .constants import header
from urllib.parse import urlparse


class AmazonScraper:
    """
        1. scape product page and find link to customer reviews page.
        2. Go to customer reviews page and scrape.
        3. Send the scraped data to the ml model for out
    """
    def __init__(self, url):
        self.url = url
        self.header = header

    def scrape_page_content(self, url):
        request = requests.get(url, headers=self.header)
        return BeautifulSoup(request.content, 'html.parser')

    def get_customer_reviews_link(self):
        soup = self.scrape_page_content(self.url)
        review_link = [a['href'] for a in soup.find_all('a') if a.text.strip() == 'See more reviews' and a.get('href')][0]
        customer_reviews_path = f'https://{urlparse(self.url).netloc}/{review_link}'

        return customer_reviews_path
    
    def generate_customer_reviews(self, reviews_url):
        soup = self.scrape_page_content(reviews_url)
        # TODO: delete just for testing.
        with open('reviews-content.txt', mode='w') as f:
            f.write(str(soup))
        reviews = self.parse_customer_review_content(soup)
        return reviews
    
    def parse_customer_review_content(self, soup):
        all_reviews = []
        reviews = soup.find_all("div", {"id": lambda x: x and x.startswith("customer_review")})

        for index, review in enumerate(reviews, start=1):
            reviewer = review.find("span", class_="a-profile-name")
            reviewer_name = reviewer.get_text(strip=True) if reviewer else "No name available"
            
            title = review.find("span", {"data-hook": "review-title"})
            review_title = title.get_text(strip=True) if title else "No title available"
            
            content = review.find("div", class_="cr-full-content")
            review_content = content.get_text(strip=True) if content else "No content available"
            
            date = review.find("span", {"data-hook": "review-date"})
            review_date = date.get_text(strip=True) if date else "No date available"
            
            review_data = {
                "id": index,
                "reviewer": reviewer_name,
                "title": review_title,
                "date": review_date,
                "content": review_content
            }
            
            all_reviews.append(review_data) 

        return all_reviews
        
