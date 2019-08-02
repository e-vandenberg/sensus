import cPickle
import re

class Analyzer:

    def __init__(self):
        import csv

        # load in the lexicon
        csvfile = open('data/lexicon_easy.csv', 'rb')
        self.reader = csv.reader(csvfile, delimiter=',')

        # load in the cached classifier
        with open('cached_models/my_dumped_classifier.pkl', 'rb') as fid:
            try:
                self.gnb_loaded = cPickle.load(fid)
            except EOFError:
                pass

        # load in the cached vectorizer
        with open('cached_models/dumped_vectorizer', 'rb') as dv:
            try:
                self.vectorizer = cPickle.load(dv)
            except EOFError:
                pass

    def clean_tweet(self, tweet):
        # clean the tweet of special characters and such

        tweet = re.sub(r'\s+[a-zA-Z]\s+', ' ', tweet)
        tweet = re.sub(r'\^[a-zA-Z]\s+', ' ', tweet)
        tweet = re.sub(r'\W', ' ', tweet)
        tweet = re.sub(r'\s+', ' ', tweet, flags=re.I)
        tweet = re.sub(r'^b\s+', '', tweet)

        return tweet.lower()

    def but_parse(self, tweet):
        # ignore everything before a 'but'
        if "but " in tweet:
            tweet = tweet.split("but ",1)[1]
        return tweet

    def lexicon_tweak(self, tweet):
        # tweak the tweet based on lexicon scores

        lexicon = dict()
        # Read in the lexicon.
        for row in self.reader:
            lexicon[row[0]] = int(row[1])
        score = 0

        tweet_content = tweet.split(' ')

        for word in tweet_content:
            if word in lexicon:
                score = score + lexicon[word]

        # allow higher score limits for longer tweets
        s_limit = 1
        if len(tweet_content) > 6:
            s_limit = 2

        if (score > s_limit):
            tweet = tweet + " happy yes"
        elif (score < -1 * s_limit):
            tweet = tweet + " sad why"
        else:
            pass
        return tweet

    def make_prediction(self, tweet):

        # apply all manual techniques to tweet
        tweet = self.lexicon_tweak(self.but_parse(self.clean_tweet(tweet)))

        # return True for positive tweet, False for negative tweet
        if self.gnb_loaded.predict(self.vectorizer.transform([tweet]).toarray())[0] == 4:
            return True
        return False
