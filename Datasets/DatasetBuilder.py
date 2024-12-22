from MarketApi.BinanceAPI import BinanceAPI
import pandas as pd
from datetime import datetime
from math import ceil
def getCandelesticks(interval="15m",
                 start=datetime(year=2024,month=11,day=1,hour=00,minute=00,second=00).timestamp()*1000,
                 end=datetime(year=2024,month=12,day=22,hour=21,minute=20,second=00).timestamp()*1000,
                 limit=1000):
    period = end - start
    time=0
    api = BinanceAPI()
    match(interval[-1]):
        case "s":
            time = int(interval[0:len(interval)-1:1]) *1000
         
        case "m":
            time = int(interval[0:len(interval)-1:1]) *60* 1000

        case "h":
            time = int(interval[0:len(interval)-1:1]) *3600* 1000
                       
        case "d":
            time = int(interval[0:len(interval)-1:1]) *24*3600* 1000       
            
        case "w":
            time = int(interval[0:len(interval)-1:1]) *7*24*3600* 1000
             
        case "M":
            time = int(interval[0:len(interval)-1:1]) *30*24*3600* 1000
                   
        case _:
            print("interval not recognized :"+interval)
    time = ceil(time) 
    nbr_interval = ceil(period / time)
    print(nbr_interval)
    if(nbr_interval > 1000):
        nbr_requests = ceil(nbr_interval / 1000)
        data = []
        temp_start = start    
        for i in range(0,nbr_requests):
            temp_end =  temp_start+ 1000*time
            api.setRequest(interval=interval,start=temp_start,end=temp_end,limit=1000)
            data = data + api.getStructuredResponse()
            temp_start = temp_start + 1000*time
            
        return data
    else:
        api.setRequest(interval=interval,start=start,end=end,limit=limit)
        response = api.getStructuredResponse()
        
        return response
    
def getLagDataset(data,feature,lag=6):
        candles_buffer = []
        lag_data = []
        for candle in data:
            candles_buffer.append(candle)
            if(len(candles_buffer)>lag):
                
                del candles_buffer[0]
            candle_buffer = {}
            for x  in candles_buffer:
                candle_buffer["time"]=x["open_time"]
                candle_buffer[feature+"_t"+str(candles_buffer.index(x))]= x[feature]
            lag_data.append(candle_buffer)
        for i in range(lag):
            del lag_data[0]
        return lag_data




if __name__ == "__main__":
    response = getCandelesticks("15m",
                                start=datetime(year=2024,month=12,day=22,hour=00,minute=0).timestamp()*1000)
    lag_data = getLagDataset(response,"open_price")
    data = pd.DataFrame(lag_data)
    data.to_csv("lag_valid_dataset.csv",index=False)

