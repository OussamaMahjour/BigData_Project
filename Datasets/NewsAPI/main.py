import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def setNEWSURL(api_key, keyword):
    api_url = f'https://newsapi.org/v2/top-headlines/?apiKey={
        api_key}&q={keyword}'
    return api_url


def setAlphavantageURL(api_key, currency):
    api_url = f'https://www.alphavantage.co/query?function=CRYPTO_INTRADAY&apikey={
        api_key}&symbol={currency}&market=USD&interval=5min'
    return api_url


Api_key = "cf709dcc21814975ad7d3c4516187776"
API_KEY2 = "BF2AFS6ISTE6MRT9"


def getNews():
    response = requests.get(setAlphavantageURL(Api_key, "BTC"))
    f = open("article.json", "w")
    # f.write(response.json()["articles"][1]["content"])
    f.write(str(response.json()))
    f.close()
   # vs = SentimentIntensityAnalyzer().polarity_scores(sentence)


if __name__ == "__main__":
    getNews()
