from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

sentence = "bitcoin is a scam  it doesn't get you anything but it does have some advantages"
vs = SentimentIntensityAnalyzer().polarity_scores(sentence)

print(str(vs))
