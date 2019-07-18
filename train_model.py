from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import ComplementNB
from sentiment_model import Analyzer
import pandas as pd
import random
import cPickle

# This file is to modify, train, then cache the scikit model
# It is not directly run in production
# The cached model is run from sentiment_model.py

# TODO:
# account for rotaion matrix words such as "not":
# fit only the word after "not", then replace expression with known opposite (positive or negative word)
#
# this uses: ComplementNB classification, n-gram vectorization, but parsing, Lexicon
#
# update clean_tweet: normalize (play, player, playing etc.)apply RNN for tweet normalization?
# add a more contextually relevant lexicon
# analysis around the subject in question
# Multi-layer --> use complementNB for easy predictions, then pass on to SVM for difficult decisions

tweets = pd.read_csv("./data/prac_data.csv")
features = tweets.iloc[:, 5].values
labels = tweets.iloc[:, 0].values

analyzer = Analyzer()

cleaned_features = []
for f in features:
    cleaned_features.append(analyzer.clean_tweet(f))

# shuffle the features alongside labels
r = zip(cleaned_features, labels)
random.Random(4).shuffle(r)
cleaned_features, labels = zip(*r)

v = CountVectorizer(max_features=7000, min_df=8, max_df=0.2, ngram_range=(1,2))
p = v.fit_transform(cleaned_features[:int(len(cleaned_features) * 0.85)]).toarray()

x_train, y_train = p, labels[:int(len(labels) * 0.85)]

remaining_features = list(cleaned_features[int(len(cleaned_features) * 0.85):])

for i in range(len(remaining_features)):
    remaining_features[i] = analyzer.lexicon_tweak(analyzer.but_parse(remaining_features[i]))

x_test, y_test = v.transform(remaining_features), labels[int(len(labels) * 0.85):]
text_classifier = ComplementNB().fit(x_train, y_train)

predictions = text_classifier.predict(x_test)
print accuracy_score(y_test, predictions)

# Save the model
with open('cached_models/my_dumped_classifier.pkl', 'wb') as fid:
    cPickle.dump(text_classifier, fid)

# Save the count vectorizer
with open('cached_models/dumped_vectorizer', 'wb') as dv:
    cPickle.dump(v, dv)
