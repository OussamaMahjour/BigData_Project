import requests
from dotenv import load_dotenv
import os
from datetime import datetime, timezone
from time import time
import pandas as pd

class BinanceAPI:
    URL = ""
    CURRENCY = ""
    API_KEY = ""
    REQUEST = ""

    def __init__(self):
        load_dotenv()
        self.API_KEY = os.getenv("API_KEY")
        self.CURRENCY = os.getenv("CURRENCY")
        self.URL = os.getenv("CURRENCY_API_URL")

    def setRequest(self,
                    interval="15m",
                    start=(time()*1000)-(15*60*1000),
                    end=time()*1000,
                    timeZone=0,
                    limit=10):
        
        self.REQUEST = self.URL + \
            f"""?symbol={self.CURRENCY}\
                &interval={interval}\
                &startTime={round(start)}\
                &endTime={round(end)}\
                &timeZone={timeZone}\
                &limit={limit}\
                """
        self.REQUEST = self.REQUEST.replace(" ","")
    def getRawResponse(self):
        if(self.REQUEST != ""):
            response = requests.get(self.REQUEST)
            return response.json()
        else:
            print("no request was set please set a request first")
            exit(2)
            
    def getStructuredResponse(self):
        if (self.REQUEST != ""):
            response = requests.get(self.REQUEST)
            klines = response.json()
            result = []
            for data in klines:
                candelstick = {       
                   "open_time" : data[0],
                   "open_price": data[1],
                   "high_price": data[2],
                   "low_price": data[3],
                   "close_price": data[4],
                   "volume": data[5],
                   "close_time":data[6],
                   "quote_asset_volume":data[7],
                   "taker_buy_asset_volume":data[8],
                   "taker_buy_quote_volume":data[9],
                   "number_of_trades":data[10],
                }
                candelstick["price"]=(float(candelstick["open_price"])+float(candelstick["close_price"]))/2
                result.append(candelstick)
            return result
        else:
            print("no request was set please set a request first")
            exit(2)


if __name__ == "__main__":
    driver = BinanceAPI()
    driver.setRequest(interval="5m",start=time()*1000 - 60*60*60*1000,limit=1000)
    kilines = driver.getStructuredResponse()
    df = pd.DataFrame(kilines)
   
    df.to_csv("dataset.csv",index=False)

