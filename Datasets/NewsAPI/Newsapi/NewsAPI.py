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
        #get the variables from the .env file
        load_dotenv()
        self.URL = os.getenv("NEWS_API_URL")
        self.CURRENCY = os.getenv("CURRENCY")
        self.API_KEY = os.getenv("API_KEY")
    
    def setRequest(self,topic,timestamp=time()):
        self.REQUEST = self.URL + f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&topics={topic}&apikey={self.API_KEY}"
        print(self.REQUEST)
    def getResponse(self):
        if(self.REQUEST == "" ):
            print("please set a request first")
            exit(2)
        
        response = requests.get(self.REQUEST)
        return response.json()
  
    def getIntervalSentiments(self,interval=300,start=time()-24*60*60*60,end=time()):
        response = self.getResponse()


        feed = response["feed"]  #getting the feed section that containt the articles
        interval_start = start #the start of the time interval
        interval_end = start+interval #the end of the time interval
        data = {}
        sentiment_score_buffer = 0 # the buffer that will holde the somme of all articles in the same interval
        nbr_articles = 0
        for article in feed:
            time = datetime.strptime(article["time_published"],"%Y%m%dT%H%M%S").timestamp() # conveting to timestamp
        
           
            if(time>=interval_start and time<interval_end):
                sentiment_score_buffer += article["overall_sentiment_score"]
                nbr_articles += 1
                
            else:
                data["start"]=interval_start
                data["end"]=interval_end
                data["sentiment_score"]=sentiment_score_buffer/nbr_articles if nbr_articles !=0 else 0 # checking if there was no articles in the interval then set it to neutral (0)
                nbr_articles=0
                sentiment_score_buffer = 0
                interval_start = interval_end
                interval_end = interval_end + interval
                print("start: "+str(datetime.fromtimestamp(data["start"]))+"  end: "+str(datetime.fromtimestamp(data["end"]))+"   sentiment_score: "+str(data["sentiment_score"]))




if __name__ == "__main__":
    api = NewsAPI()
    api.setRequest("bitcoin")
    response = api.getResponse()
    api.getIntervalSentiments()