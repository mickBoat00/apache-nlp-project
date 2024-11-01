import os
from openai import OpenAI
from pydantic import BaseModel

class Review(BaseModel):
    title: str

class Cluster(BaseModel):
    cluster_name: str
    cluster_reviews: list[Review]

class TopicCluster(BaseModel):
    clusters: list[Cluster]

class OpenAIModel:
    def __init__(self, reviews):
        self.client = OpenAI(api_key=os.environ['OPENAIAPI_SECRET_KEY'])
        self.reviews = reviews
        
    def categorize_reviews(self):
        completion = self.client.beta.chat.completions.parse(
        model="gpt-4o-mini-2024-07-18",
        messages=[
                {
                    "role": "system", 
                    "content": "You are a trained clustering model that group a list of reviews objects into topic clusters. By using the values of the objects content key summarize it and group into a topic. Produce a list of object which are the clusters and each cluster contains the reviews with just the title under it."},
                {
                    "role": "user",
                    "content": str(self.reviews)
                }
            ],
            response_format=TopicCluster,
        )
        return completion.choices[0].message.parsed
