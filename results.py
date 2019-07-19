import tweepy
from sentiment_model import Analyzer
import api_keys as keys

auth = tweepy.OAuthHandler(keys.consumer_key, keys.consumer_secret)
auth.set_access_token(keys.access_token, keys.access_token_secret)
api = tweepy.API(auth)

analyzer = Analyzer()

def gather_tweets(keyword, geocode):
    # gathers a max of 100 tweets by keyword and geocode
    result = api.search(q=keyword, geocode=geocode, tweet_mode='extended', count=100)
    return result

def add_to_dict(d, keyword, chunk):
    # creates a dict in the format "Region" : ['tweet1', 'tweet2', ...]
    # used to simplify multithreading process
    for e in chunk:
        radius = "100mi"
        if e["longitude"] < -95:
            radius = "143mi"
        if e["longitude"] > -75:
            radius = "70mi"
        d[str(e["state"])] = gather_tweets(keyword, str(e["latitude"]) + "," + str(e["longitude"]) + "," + radius)

def process(region, d, results, regions):
    # processes the tweets in a region using the sentiment analysis

    positive, negative = 0, 0

    for tweet in d[region]:
        result = analyzer.make_prediction(tweet.full_text.encode("utf-8"))
        if result:
            positive += 1
        else:
            negative += 1

    region_index = next((i for i, item in enumerate(regions) if item["state"] == region))

    if positive + negative > 9:
        percentage = round(float(positive * 100)/(positive + negative), 2)

        results[region] = [region_index, percentage]

    else:
        # not enough recent tweets
        results[region] = [region_index, 0]

def main(keyword):
    import json
    import time
    from threading import Thread


    with open('data/regions.json') as f:
        regions = json.load(f)

    # setup threading requirements
    d = {}
    threads = []

    # change this based on how fast you want tweets to be gathered
    # works best as multiple of len(regions)
    nthreads = 50


    for i in range(nthreads):
        chunk = regions[i::nthreads]
        t = Thread(target=add_to_dict, args=(d, keyword, chunk))
        threads.append(t)

    # launch threads and ensure they finish before moving forward

    [t.start() for t in threads]
    [t.join() for t in threads]


    # results is a dict that comes back in the format: {state: [state_index, positive_percentage]}
    # state_index is used for communication with the geoJSON on the frontend
    results = {}
    for r in regions:
        process(str(r["state"]), d, results, regions)

    return results

if __name__ == "__main__":
    import sys
    keyword = sys.argv[1]
    print "analyzing tweets with keyword:", keyword
    print main(keyword)
