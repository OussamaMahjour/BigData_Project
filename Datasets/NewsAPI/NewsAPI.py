import requests
from dotenv import load_dotenv
import os
from datetime import datetime, timezone
from time import time
import pandas as pd

class NewsAPI:
    URL = ""
    CURRENCY = ""
    API_KEY = ""
    REQUEST = ""
    def __init__(self):
        load_dotenv()
        self.URL = os.getenv("NEWS_API_URL")
        self.CURRENCY = os.getenv("CURRENCY")
        self.API_KEY = os.getenv("NEWS_API_KEY")
    
    def setRequest(self,topic,timestamp=time()):
        self.REQUEST = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&topics={topic}&apikey={self.API_KEY}"
        print(self.REQUEST)
    def getResponse(self):
        response = requests.get(self.REQUEST)
        return response.json()

if __name__ == "__main__":
    api = NewsAPI()
    api.setRequest("bitcoin")
    f = open("news.json","w")
    print(api.getResponse())
    f.write(str(api.getResponse()))
    f.close()
